import pandas as pd
import spacy



class PreoperativeEpicrisisParser:
    """
    парсер для данных предоперационного эпикриза
    ...
    атрибуты
    ----------
    data (str) : данные предоперационного эпикриза
    path_to_dict (str) : путь до словаря мед терминов

    методы
    -------
    _preprocessing(): лемматизация, нижний регистр и удаление стоп-слов
    _find_absent(index): находит есть ли производные от "отсутствует" после фичи
    _closest_num(index): находит ближайшие числа после фичи, если они есть
    structure(): возвращает словарь вида признак:значение
    """
        
    def _preprocessing(self):        
        self._preprocessed_tokens = []
        n_tokens = 1
        for token in self._doc:
            if not token.is_stop and not token.is_punct:
                self._preprocessed_tokens.append([n_tokens, token.text.lower(), token.lemma_, token.pos_, token.dep_, token.head.lemma_])
                n_tokens += 1
        self.l = n_tokens
        
    
    def __init__(self, data: str, path_to_dict: str, model='init'):
        """
        параметры
        -------
        data (str) : данные предоперационного эпикриза
        path_to_dict (str) : путь до словаря мед терминов
        model : если 'init' (по дефолту), то модель инициализируется внутри класса (как и надо - подается только два параметра),
                иначе модель иниц. вне класса и подается как входной параметр 
                (нужно чисто для первого теста, чтобы не надо было иниц. модель 250 раз (гигадолго))
        """
        
        self.data = data
        self._terms_df = pd.read_csv(path_to_dict, sep=' ', header=None)
        div = self._terms_df[self._terms_df.iloc[:,0]=='------'].index
        self._terms_nums = [i for i in self._terms_df.iloc[:div.values[0],0]]
        self._terms_present = [i for i in self._terms_df.iloc[div.values[0]+1:,0]]
        if model == 'init':
            self._model = spacy.load('ru_core_news_lg')
        else:
            self._model = model
        self._doc = self._model(self.data)
        self._preprocessing()
        self.di = {}
        self._duplicate = 1
    
    
    def _find_absent(self, index):
        """
        параметры
        -------
        index (int) : индекс текущего токена

        возвращает
        -------
        (int) : 1 если есть производные слова отсутствует, иначе 0
        """
        
        token = self._preprocessed_tokens
        offset = 0
        res = []
        list_absent = ['отрицательно','отрицает','нет','нету','отсутствует','отс','отст','отриц','отрицат','отрицательный','отрицательн']
        
        while (offset < 3 and index+offset < self.l-2):
            offset += 1
            if token[index+offset][1] in list_absent:
                return 0
        return 1
    
    
    def _closest_num(self, index):
        """
        параметры
        -------
        index (int) : индекс текущего токена

        возвращает
        -------
        (str) : строка с числовыми значениями для текущей фичи
        """
        
        token = self._preprocessed_tokens
        offset = 0
        res = []
        
        while (token[index+offset][3] != 'NUM'):
            offset += 1
            if (index+offset == self.l-1) or (offset > 4):
                return '-'
            
        while (token[index+offset][3] == 'NUM'):
            res.append(token[index+offset][1])
            offset += 1
            if (index+offset) == self.l-1:
                break

        return ' '.join(res)
            
    
    def structure(self):
        """
        возвращает
        -------
        di (dict) : словарь вида признак:значение
        """
        token = self._preprocessed_tokens
        for i in range(len(token)):
            key = ''
            value = 0
            if i+2 == self.l:
                break
            tk = token[i]
            pred_tk = token[i-1][1]
            post_tk = token[i+1][1]
            tk_i, tk_text, tk_lem, tk_pos, tk_dep, tk_head = tk
            
            # общая обработка через словарь мед терминов
            # сначла для фичей, где могут быть числовые значения, потом на присутствие болезней
            if tk_lem in self._terms_nums:
                key = tk_lem
                value = self._closest_num(i)
                
            
            if tk_lem in self._terms_present:
                key = tk_lem
                value = self._find_absent(i)
                
            # дальше идет обработка частных случаев, которые не попадают под обработку через словарь    
            # возраст
            if tk_text in ['лет','год']:
                key = 'возраст'
                value = pred_tk
            
            # специальные qrs
            if tk_text in ['friderici','bazett','sagi']:
                key = f'QTc {tk_text}'
                value = self._closest_num(i)
            
            # все с лж
            if tk_text == 'лж':
                if token[i+1][3] != 'NUM':
                    key = f'{pred_tk} {tk_text} {post_tk}'
                else:
                    key = f'{pred_tk} {tk_text}'
                if pred_tk in list(self.di.keys()):
                    del self.di[pred_tk]
                value = self._closest_num(i)
            
            # гб
            if tk_lem == 'болезнь' and token[i-1][2] == 'гипертонический':
                key = 'гб'
                value = 1
                 
            # имт
            if tk_text == 'индекс' and post_tk == 'массы' and token[i+2][1] == 'тела':
                key = 'индекс массы тела'
                value = self._closest_num(i)
                
            # ппт
            if tk_lem == 'площадь' and token[i+1][2] == 'поверхность' and token[i+2][2] == 'тело':
                key = 'площадь поверхности тела'
                value = self._closest_num(i)
            
            # пароксизм
            if tk_lem == 'пароксизм':
                key = f'пароксизм {post_tk}'
                value = 1
            
            # стеноз
            if tk_lem == 'стеноз':
                key = f'{tk_lem} {post_tk}'
                value = 1 
                
            # гепатит
            if tk_lem == 'гепатит':
                key = f'{tk_lem} {post_tk}'
                value = self._find_absent(i)
            
            # жэ
            if tk_lem == 'жэ':
                if post_tk in ['1','2']:
                    key = f'{pred_tk} ЖЭ {post_tk} типа'
                    value = self._closest_num(i+2)
                else:
                    key = f'{pred_tk} ЖЭ'
                    value = self._closest_num(i)
            
            # группа крови
            if tk_lem == 'кровь' and pred_tk == 'группа':
                try:
                    if post_tk == 'ab0':
                        key = f'{pred_tk} {tk_text} {post_tk}'
                    else:
                        key = f'{pred_tk} {tk_text}'
                    cur_min = min(5,self.l-(i+1))
                    for j in range(cur_min):
                        if token[i+j][1] in ['0','a','b','ab','nt']:
                            value = token[i+j][1]
                            break
                except Exception as e:
                    print(e)
            
            if key != '':
                if key in self.di.keys():
                    while (key in self.di.keys()):
                        key = f'{key} ({self._duplicate})'
                        self._duplicate += 1
                    self._duplicate = 1
                self.di[key] = value
                
        del self._model
        del self._doc
        
        for k in self.di:
            try:
                num_value = int(self.di[k])
            except ValueError:
                try:
                    num_value = float(self.di[k])
                except ValueError:
                    num_value = self.di[k]
            self.di[k] = num_value  
                
        return self.di