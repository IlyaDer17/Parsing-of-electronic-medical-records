import spacy
from spacy.matcher import Matcher, PhraseMatcher
from pprint import pprint


class MedicalTermMatcher:
    def __init__(self, path_to_dict):
        with open(path_to_dict) as f:
            self.lst_dict = []
            for j in f:
                    if ' ' in j:
                        for i in j.split():
                            self.lst_dict.append(i)
                    else:
                        self.lst_dict.append(j.strip())
        self.patterns_word = [{"LEMMA": i, "LENGTH": {">=": 4}} for i in self.lst_dict]
        self.nlp = spacy.load("ru_core_news_lg")
        self.matcher_word = Matcher(self.nlp.vocab)
        self.matcher_word.add("Медицинский термин", [[pattern] for pattern in self.patterns_word])
    
    def match(self, text):
        doc = self.nlp(text)
        matches_word = self.matcher_word(doc)
        #matches_phrase = self.matcher_phrase(doc)
        dct = {}
        for match_id, start, end in matches_word:
            string_id = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            dct.setdefault("Медицинские термины", []).append(span.text)

        return dct
    

#При создании объекта класса следует указать путь к словарю медицинских терминов (приложу рядом с файлом (словарь в был сделан на коленке, но справляется))
#после в переменную text дать текст, который надо проанализировать
#Написанный класс выделяет процентов 70 медицинских терминов в тексте, с тем как выделять полноценные фразы до конца не разобрался, так что пока без них
#Выходит выделять числовые значения с размерностями, но не получилось пока в классе прописать.
#ИТОГ: программа просто выделяет в словарь медтермины

mtm = MedicalTermMatcher('E:\\Leanr myself\\Python\\NLPMed\\dictionary.txt')
text = 'КЛИНИЧЕСКИЙ ДИАГНОЗ:Основной: Деменция при болезни , с выраженным интеллектуально мнестическими нарушениями 120 80 мм рт, эпизодами конфабуляторной спутанности, моторной афазией 120 кг, дизартрией. ОСНОВНОЙ УТОЧНЕННЫЙ : Код по МКБ10: F00.10 Деменция при болезни А'
result = mtm.match(text)
pprint(result)