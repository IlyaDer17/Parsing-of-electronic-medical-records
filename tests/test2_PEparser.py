import random
import pandas as pd
import sys
import os

DIR = os.path.dirname(os.path.dirname(__file__))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from parsers.PE_parser import PreoperativeEpicrisisParser as parser


def test2():
    df = pd.read_pickle('recs/med_recs_depers.pkl')
    data = df[df['Статус']=='ПРЕДОПЕРАЦИОННЫЙ ЭПИКРИЗ']
    data = list(data['Данные'].values)
    path_to_terms = f'{DIR}/terms/terms.txt'
    
    ind = random.randint(1,len(data))
    print(data[ind])
    
    try:
        print(parser(data[ind], path_to_terms).structure())
    except Exception as e:
        print('Невозможно обработать')
        print(e)
        
        
test2()