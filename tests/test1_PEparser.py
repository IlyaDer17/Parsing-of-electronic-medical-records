import pandas as pd
import spacy
import sys
import os

DIR = os.path.dirname(os.path.dirname(__file__))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from parsers.PE_parser import PreoperativeEpicrisisParser as parser


def test1():
    df = pd.read_pickle('recs/med_recs_depers.pkl')
    data = df[df['Статус']=='ПРЕДОПЕРАЦИОННЫЙ ЭПИКРИЗ']
    data = list(data['Данные'].values)
    model = spacy.load('ru_core_news_lg')
    path_to_terms = f'{DIR}/terms/terms.txt'
    
    for ind in range(len(data)):
        if ind%50 == 0 or ind==len(data)-1:
            print(f'Запись {ind}/{len(data)-1}')
        try:
            parser(data[ind], path_to_terms, model).structure()
        except Exception as e:
            print(f'Упал на записи {ind}')
            print(e)
            break
            
            
test1()