import pickle
import numpy as np
from Stationary_Diagnosis import Stationary_Diagnosis

with open('med_recs_depers.pkl', 'rb') as f:
    x = pickle.load(f)
d = x.loc[x.Статус == 'ЖАЛОБЫ', 'Данные']
path_dictionary = "dictionary.csv"
i = 0
if __name__ == '__main__':
    while i == 0:
        try:
            Object = Stationary_Diagnosis(d.iloc[np.random.random_integers(np.size(d))], path_dictionary)
            print('________________________________________________')
            i = 1
        except:
            print(0)
            i = 0
