import numpy as np
import pandas as pd
import spacy
import json
import pickle



class PreoperativeEpicrisisParser:
    """
    Парсер для данных предоперационного эпикриза

    ...

    Attributes
    ----------
    data : str
        Данные предоперационного эпикриза в виде строки

    Methods
    -------
    print_tokens():
        Вывод токенов
    preprocessing():
        Обработка данных в нужное представление
    find_features():
        Результат обработки неструктурированных записей в виде json
    result_as_dataframe():
        Результат обработки в виде пациент - датафрейм
    """

    
    def __init__(self, data: str):
        """
        Parameters
        ----------
        data : str
            Данные в виде строки
        """

        self.data = data + ' ПРЕДОПЕРАЦИОННЫЙ ЭПИКРИЗ'
        self.model = spacy.load('ru_core_news_lg')
        self.doc = self.model(self.data)
        self.di = {}
        
    
    def print_tokens(self):
        """
        Вывод всех токенов в виде (индекс, токен, часть, зависимость, родитель)
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        for token in self.doc:
            token_ind = token.i
            token_text = token.text
            token_pos = token.pos_
            token_dep = token.dep_ 
            token_head = token.head.text
            print(f"{token_ind:<10}{token_text:<12}{token_pos:<10}" \
                  f"{token_dep:<10}{token_head:<12}")
    
    
    def preprocessing(self):
        """
        Деление данных из строки на записи вида пациент - значения.
        Сохраняется в виде словаря di
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        patients = []
        records = []
        # начало и конец текущего окна
        ind_past = 0
        ind_new = 0
        
        # запсиси делятся по сочетанию ПРЕДОПЕРАЦИОННЫЙ ЭПИКРИЗ
        for token in self.doc:
            if self.doc[token.i].text == 'ПРЕДОПЕРАЦИОННЫЙ' and self.doc[token.i+1].text == 'ЭПИКРИЗ':
                ind_new = token.i
                cur_spaces = []

                for t in self.doc[ind_past:ind_new]:
                    if t.pos_ == "SPACE":
                        cur_spaces.append(t.i)
                
                if len(cur_spaces) <= 3:
                    cur_spaces = [len(self.doc),len(self.doc),len(self.doc)]
                    ind_past -= 3
                
                # далее в список patients кладутся id пациентов
                # в id могут быть скобки и запятые, которые считаются как токены, 
                # поэтому сначала обработываются эти случаи, чтобы id правильно записался
                # в общем они ищутся как третий с конца токен, не считая пробелы
                
                if self.doc[cur_spaces[-3]-1].text in ["]"]:
                    patients.append(self.doc[cur_spaces[-3]-2].text+self.doc[cur_spaces[-3]-1].text)
                elif self.doc[cur_spaces[-3]-1].text in [","]:
                    patients.append(self.doc[cur_spaces[-3]-3].text+self.doc[cur_spaces[-3]-2].text)
                else:    
                    patients.append(self.doc[cur_spaces[-3]-1].text)
                    
                # в список records кладутся наблюдения
                # это токены от начала окна до id пациента
                # опять же если была запятая в id немного другая обработка
                if self.doc[cur_spaces[-3]-1].text in [","]:
                    records.append(self.doc[ind_past+3:cur_spaces[-3]-4].text)
                else:
                    records.append(self.doc[ind_past+3:cur_spaces[-3]-2].text)
        
                ind_past = ind_new
       
        self.patients = patients
        self.records = records
        
        # конечный словарь
        for pat, rec in zip(self.patients, self.records):
            self.di.setdefault(pat, []).append(rec)
        
           
    def find_features(self):
        """
        Нахождение сущностей
        
        Parameters
        ----------
        None

        Returns
        -------
        result : json
            Размеченные данные в виде json
        """
        
        result = {}
        patient_ind = 0
        
        for key in np.unique(np.array(self.patients)):
            patient_ind += 1
            
            # токенизация для наблюдений текущего пациента
            nlp = self.model(' '.join(self.di[key]))

            cur_result = {'ID': key, 'Название признака':[], 
                          'Значение': [], 'Единицы измерения':[]}
            
            patient_label = f'Пациент {patient_ind}'
            
            for token in nlp:
                if token.i != len(nlp)-1:
                    if nlp[token.i].pos_ == 'PUNCT':
                        ind1 = -1
                    elif nlp[token.i].pos_ == 'PROPN':
                        ind1 = 0
                    
                    # если PROPN PUNCT NUM или PROPN NUM
                    # например Рост : 180 или Рост 180
                    if nlp[token.i].pos_ in ['PUNCT','PROPN'] and nlp[token.i+1].pos_ == 'NUM':
                        ind2 = 1
                        ind_v = 1
                        cur_prefix = [] # префикс - название признака
                        cur_values = [] # само значение
                        cur_postfix = [] # постфикс - единицы измерения
                        
                        # считаются границы префикса
                        while nlp[token.i+ind1].pos_ != 'PUNCT' and token.i+ind1 >= 0:
                            if nlp[token.i+ind1].pos_ != 'NUM':
                                cur_prefix.append(nlp[token.i+ind1].text)
                            ind1 -= 1
                        
                        # считаются границы постфикса
                        while nlp[token.i+ind2].pos_ != 'PROPN':
                            if nlp[token.i+ind2].pos_ != 'NUM':
                                cur_postfix.append(nlp[token.i+ind2].text)
                            ind2 += 1
                            if token.i+ind2 == len(nlp)-2:
                                break

                        cur_prefix.reverse()
                    
                        # значение
                        while nlp[token.i+ind_v].pos_ == 'NUM':
                            cur_values.append(nlp[token.i+ind_v].text)
                            ind_v += 1

                        # оформление
                        if cur_prefix:
                            pref_str = ' '.join(cur_prefix)
                            pref_str = pref_str.replace('мсек','')
                            cur_result['Название признака'].append(pref_str)

                            cur_result['Значение'].append(' '.join(cur_values))
                            
                            # обработка исключений типа ненужных знаков препинания и тд
                            # нужно чтобы исключались не отсносящиеся к текущим единицам слова
                            if cur_postfix:
                                post_str = ' '.join(cur_postfix)
                                post_cut1 = ' '.join(cur_postfix).find(',')
                                post_cut2 = ' '.join(cur_postfix).find(';')

                                if post_cut1 != -1 and post_cut2 == -1:
                                    post_str = post_str[:post_cut1]
                                elif post_cut1 == -1 and post_cut2 != -1:
                                    post_str = post_str[:post_cut2]
                                elif post_cut1 != -1 and post_cut2 != -1:
                                    post_str = post_str[:min(post_cut1,post_cut2)]
                                if post_str:
                                    cur_result['Единицы измерения'].append(post_str[:10])
                                else:
                                    cur_result['Единицы измерения'].append('-')

                            else:
                                cur_result['Единицы измерения'].append('-')

            result[patient_label] = cur_result
            
                
        self.features = result
        return json.dumps(result, indent=4, ensure_ascii=False)
    
    
    def result_as_dataframe(self):
        """
        Преобразует результат в словарь: пациент - датафрейм
        
        Parameters
        ----------
        None

        Returns
        -------
        result : dict
            Размеченные данные в виде словаря, состоящего из датафреймов
        """
        
        result_dfs = {}
        
        for n_patient, n_record in self.features.items():
            i, x, y, z = [val for val in n_record.values()]
            result_dfs[n_patient] = pd.DataFrame(list(zip(x, y, z)), 
                                                 columns = ['Название признака','Значение','Единицы измерения'])
            
        return result_dfs






data = pd.read_pickle('recs/med_recs_depers.pkl')
data = data[data['Статус']=='ПРЕДОПЕРАЦИОННЫЙ ЭПИКРИЗ']


text1 = data.to_string()
text2 = ' '.join(data['Данные'].values)
text3 = 'QRS : 100 мсек QT : 300 мсек L : S I g III гр. Фибрилляция трепетание предсердий, тахисистолическая форма, ЧЖС 162 уд в мин. Эл. ось S I g III. Признаки гипертр ЭХОКГ : Дата проведения , Рост : 172 см , Масса тела : 127.0 кг , Индекс массы тела : 42.9 кг м2'


parser = PreoperativeEpicrisisParser(text1)
parser.preprocessing()


# json
result = parser.find_features()
# print(result)

# датафреймы
dataframes = parser.result_as_dataframe()
# dataframes['Пациент 1']
# dataframes['Пациент 2']


parser = PreoperativeEpicrisisParser(text2)
parser.preprocessing()

# json
result = parser.find_features()
# print(result)

# датафреймы
dataframes = parser.result_as_dataframe()
# dataframes['Пациент 1']


parser = PreoperativeEpicrisisParser(text3)
parser.preprocessing()

# json
result = parser.find_features()
# print(result)

# датафреймы
dataframes = parser.result_as_dataframe()
# dataframes['Пациент 1']