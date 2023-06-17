from pandas import *
from pprint import pprint
from os import *


class Recomend:
    #класс будет основываться на объекте, поэтому используем обращение self без указателя object далее

    def __init__(self):
        self.df = self.file_open()
        self.structured_dict = {}
        self.receiving_recomendations()

    def file_open(self):
        # копируется путь файла (универсальный для пользователей, но необходимо указывать директорию, в которой он находится, отдельно)
        # из os, здесь прописана персональная директория, общая директория записей recs: "\recs\med_recs_depers.pkl"
        fpath = path.abspath("..") + "\\honor\\proba\\med_recs_depers.pkl"
        dataframe = read_pickle(fpath) #аналог readlines(), os.PathLike()
        return dataframe

    def receiving_recomendations(self):
        count = -1 # рекомендации лежат в самом конце массива данных, поэтому проще начать с -1, чтобы не считать лишнее
        while True:
            a = self.df["Статус"].iloc[count] # ищем индекс вхождения статуса, соответствие статуса тому, что нам нужно спарсить
            if a == "РЕКОМЕНДАЦИИ": # соответствие Статуса показателю РЕКОМЕНДАЦИИ
                self.osnova(counter = count)
                count -= 1 
            else:
                break
        pprint(self.structured_dict)
        return self.structured_dict

    def osnova(self, counter):
        if self.df["patient_ID"].iloc[counter] not in self.structured_dict.keys(): # возможно ID пациента мы уже встречали и уже обращались к нему
            self.structured_dict[self.df["patient_ID"].iloc[counter]] = {
                "Рекомендации": None # основная часть рекомендаций содержит преимущество именно их, поэтому иные показатели отсутствуют
            }
            self.structured_dict[self.df["patient_ID"].iloc[counter]]["Рекомендации"] = self.df["Данные"].iloc[counter]
                
        else: # если ID пациента уже встречалось, но мы нашли новую запись, занесём её в аннотацию к пациенту
             self.structured_dict[self.df["patient_ID"].iloc[counter]]["Рекомендации"] = self.df["Данные"].iloc[counter]

t = Recomend() # на выходе получаем запись представления данных
