import pandas as pnd
import os
from pprint import pprint


class Complaints:

    def __init__(self):
        self.df = self.open_file()
        self.structured_dict = {}
        self.receiving_part_of_the_complaints()

    def open_file(self):
        file_path = os.path.abspath("..") + "/recs/med_recs_depers.pkl"
        dataframe = pnd.read_pickle(file_path)
        # dataframe.to_csv("med_recs_depers.csv", header=True, index=None, sep=" ", mode="wb")
        return dataframe

    def receiving_part_of_the_complaints(self):
        count = 0
        while True:
            a = self.df["Статус"].iloc[count]
            if a == "ЖАЛОБЫ":
                self.structured(counter=count)
                count += 1
            else:
                break
        pprint(self.structured_dict)
        return self.structured_dict

    def structured(self, counter):
        if self.df["patient_ID"].iloc[counter] not in self.structured_dict.keys():
            self.structured_dict[self.df["patient_ID"].iloc[counter]] = {
                "Дата и время": None,
                "Жалобы": None,
                "Услуги": self.df["Услуги294_экз"].iloc[counter]
            }
            if "Дата и время" in self.df["Данные"].iloc[counter]:
                self.structured_dict[self.df["patient_ID"].iloc[counter]]["Дата и время"] = \
                    self.df["Данные"].iloc[counter][-8::]

            else:
                self.structured_dict[self.df["patient_ID"].iloc[counter]]["Жалобы"] = \
                    self.df["Данные"].iloc[counter]

        else:
            if "Дата и время" in self.df["Данные"].iloc[counter]:
                self.structured_dict[self.df["patient_ID"].iloc[counter]]["Дата и время"] = \
                    self.df["Данные"].iloc[counter][-8::]

            else:
                self.structured_dict[self.df["patient_ID"].iloc[counter]]["Жалобы"] = \
                    self.df["Данные"].iloc[counter]


test = Complaints()
# test.open_file()
# test.receiving_part_of_the_complaints()
# test.structured()
# test.data_time()
