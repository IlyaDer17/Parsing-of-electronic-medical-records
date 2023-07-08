import pickle
import numpy as np
import sys
import os

DIR = os.path.dirname(os.path.dirname(__file__))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from parsers.Stationary_Diagnosis import Stationary_Diagnosis as parser
with open(f'{DIR}/recs/med_recs_depers.pkl', 'rb') as f:
    x = pickle.load(f)
d = x.loc[x.Статус == 'ЖАЛОБЫ', 'Данные']
path_dictionary = f'{DIR}/terms/dictionary.csv'
i = 0
while i == 0:
        try:
            Object = parser(d.iloc[np.random.random_integers(np.size(d))], path_dictionary)
            print('________________________________________________')
            i = 1
        except:
            print(0)
            i = 0
