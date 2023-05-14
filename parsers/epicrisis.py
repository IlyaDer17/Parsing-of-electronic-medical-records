import pandas as pd
import pickle
import shutil
import os
import pprint


class epicrisis():

    def __init__(self):
        self.fileopened = self.openfile()
        self.structured_dict = {}
        self.extracting()
        self.structuring()

    def openfile(self):
        filepath = os.getcwd() + "\\med_recs_depers.pkl"
        my_table = pd.read_pickle(filepath)
        return my_table

    def extracting(self):
        extracted = self.fileopened.loc[self.fileopened['Статус'] == 'ВЫПИСНОЙ ЭПИКРИЗ НОВЫЙ']
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.expand_frame_repr', False)

        def format_columns(col):
            return lambda x: f"{x:<{col.str.len().max()}}"

        formats = {col: format_columns(extracted[col]) for col in extracted.columns}
        return extracted

    def structuring(self):
        for i in range(0, 249):
            if self.extracting()["patient_ID"].iloc[i] not in self.structured_dict.keys():
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]] = {
                    "ФИО пациента": '0',
                    "КЛИНИЧЕСКИЙ ДИАГНОЗ": '0',
                    "Анамнез заболевания": '0',
                    "Дата рождения": '0',
                    "возраст пациента": '0',
                    "Адрес пациента": '0',
                    "истории болезни": '0',
                    "Даты поступления и выписки": '0',
                    "Лечащий врач": '0',
                    "Услуги": self.extracting()["Услуги294_экз"].iloc[i]}
            if "истории болезни" in self.extracting()["Данные"].iloc[i]:
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["истории болезни"] = \
                    self.extracting()["Данные"].iloc[i][-19::]

            if "ФИО пациента" in self.extracting()["Данные"].iloc[i]:
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["ФИО пациента"] = \
                    self.extracting()["Данные"].iloc[i][-1::]

            if "Дата рождения" in self.extracting()["Данные"].iloc[i]:
                start_index = self.extracting()["Данные"].iloc[i].find("Дата рождения")
                end_index = start_index + len("Дата рождения: ")
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["Дата рождения"] = \
                    self.extracting()["Данные"].iloc[i][end_index:end_index + 1:1]

            if "возраст пациента" in self.extracting()["Данные"].iloc[i]:
                start_index = self.extracting()["Данные"].iloc[i].find("возраст пациента")
                end_index = start_index + len("возраст пациента: ")
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["возраст пациента"] = \
                    self.extracting()["Данные"].iloc[i][end_index:end_index+6:1]

            if "Лечащий врач" in self.extracting()["Данные"].iloc[i]:
                start_index = self.extracting()["Данные"].iloc[i].find("Лечащий врач")
                end_index = start_index + len("Лечащий врач:")
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["Лечащий врач"] = \
                    self.extracting()["Данные"].iloc[i][end_index:end_index+1:1]

            if "Даты поступления и выписки" in self.extracting()["Данные"].iloc[i]:
                start_index = self.extracting()["Данные"].iloc[i].find("Даты поступления и выписки")
                end_index = start_index + len("Даты поступления и выписки:")
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["Даты поступления и выписки"] = \
                    self.extracting()["Данные"].iloc[i][end_index:end_index+20:1]

            if "Адрес пациента" in self.extracting()["Данные"].iloc[i]:
                start_index = self.extracting()["Данные"].iloc[i].find("Адрес пациента")
                end_index = start_index + len("Адрес пациента:")
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["Адрес пациента"] = \
                    self.extracting()["Данные"].iloc[i][end_index:end_index+30:1]

            if "КЛИНИЧЕСКИЙ ДИАГНОЗ" in self.extracting()["Данные"].iloc[i]:
                parts = self.extracting()["Данные"].iloc[i].split('. ')
                self.structured_dict[self.extracting()["patient_ID"].iloc[i]]["КЛИНИЧЕСКИЙ ДИАГНОЗ"] = \
                    parts

        pprint.pprint(self.structured_dict, width=150)
        return self.structured_dict


itog = epicrisis()
