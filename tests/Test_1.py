import pickle
import numpy as np
from Stationary_Diagnosis import Stationary_Diagnosis

with open('med_recs_depers.pkl', 'rb') as f:
    x = pickle.load(f)
d = x.loc[x.Статус == 'ДИАГНОЗ СТАЦИОНАРНЫЙ', 'Данные']
# d = x.loc[x.Статус == 'ЖАЛОБЫ', 'Данные']
path_dictionary = "dictionary.csv"
if __name__ == '__main__':
    for i in range(0, np.size(d)):
        try:
            Object = Stationary_Diagnosis(d.iloc[i], path_dictionary)
            print('________________________________________________')
        except:
            i = i+1