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
path_dictionary = f'{DIR}/terms/Dictionary.txt'
Record = d.iloc[np.random.random_integers(np.size(d))]
try:
    print(Record)
    print('________________________________________________')
    Object = parser(Record, path_dictionary)
except:
    print(Record)
    print('Ошибка')
