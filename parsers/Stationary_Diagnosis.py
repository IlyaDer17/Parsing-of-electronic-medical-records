import numpy as np
import pickle
import nltk
from nltk.tokenize import word_tokenize
import string
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
import pandas as pd

class Stationary_Diagnosis(object):
    def __init__(self, d):
        N = np.size(d)
        s = np.empty([N, 1], dtype=object)
        sentenses = np.empty([10, 1], dtype=object)
        Type_diagnosis = np.empty([N, 2], dtype=object)
        Diagnosis_name = np.empty([N, 1], dtype=object)
        MKB = np.empty([N, 1], dtype=object)
        Disease_mode = np.empty([N, 1], dtype=object)
        k = 0
        for i in range(0, N):
            s[i] = str(d.iloc[i])
            ss = str(s[i])
            for one in ss.split(': '):
                k = k + 1
                sentenses[k] = one
                for two in one.split('. '):
                    if ('тоз' in two) == True or ('рит' in two) == True or ('ость' in two) == True or (
                            'индром' in two) == True:
                        Diagnosis_name[i] = two
                if ('Характер заболевания ' in sentenses[k - 1]) == True:
                    Disease_mode[i] = sentenses[k]
                if ('Код по МКБ10' in sentenses[k - 1]) == True:
                    for two in word_tokenize(str(one)):
                        if len(two) > 1:
                            if two[1].isdigit() == True:
                                MKB[i] = two
            k = 0
            words = word_tokenize(str(s[i]))
            punctuations = list(string.punctuation)
            words = [word for word in words if word not in punctuations]
            bigram_collocation = BigramCollocationFinder.from_words(words)
            for one in bigram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 10):
                if one == ('ОСЛОЖНЕНИЕ', 'ПОСТУПЛЕНИЯ'):
                    Type_diagnosis[i, :] = one
                if one == ('ОСЛОЖНЕНИЕ', 'ВЫПИСКИ'):
                    Type_diagnosis[i, :] = one
                if one == ('КЛИНИЧЕСКИЙ', 'ДИАГНОЗ'):
                    Type_diagnosis[i, :] = one
                if one == ('СОПУТСТВУЮЩИЙ', 'КЛИНИЧЕСКИЙ'):
                    Type_diagnosis[i, :] = one
                if one == ('СОПУТСТВУЮЩИЙ', 'ПОСТУПЛЕНИЯ'):
                    Type_diagnosis[i, :] = one
                if one == ('СОПУТСТВУЮЩИЙ', 'ВЫПИСКИ'):
                    Type_diagnosis[i, :] = one
        self.TD = Type_diagnosis
        self.MKB = MKB
        self.DN = Diagnosis_name
        self.DM = Disease_mode

with open('med_recs_depers.pkl', 'rb') as f:
    x = pickle.load(f)
d = x.loc[x.Статус == 'ДИАГНОЗ СТАЦИОНАРНЫЙ', 'Данные']
a = Stationary_Diagnosis(d)
TD = pd.Series(list(a.TD))
DN = pd.Series(list(a.DN))
MKB = pd.Series(list(a.MKB))
DM = pd.Series(list(a.DM))
states = pd.DataFrame({'Вид диагноза': TD, 'Номер МКБ': MKB, 'Название диагноза': DN, 'Характер заболевания': DM})
#string1 = str(s[1])
#words = word_tokenize(string1)
#punctuations = list(string.punctuation)
#words = [word for word in words if word not in punctuations]
#bigram_collocation = BigramCollocationFinder.from_words(words)
#trigram_collocation = TrigramCollocationFinder.from_words(words)
#print(s[1])
#print("___________________")
#print(words)
#print("___________________")
#print(bigram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 10))
#print("___________________")
#print(trigram_collocation.nbest(TrigramAssocMeasures.likelihood_ratio, 10))
