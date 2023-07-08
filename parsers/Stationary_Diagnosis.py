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
import csv

class Stationary_Diagnosis(object):
    def __init__(self, string, path_dictionary):
        self.str = string
        with open(path_dictionary, 'r') as r_file:
            file_reader = csv.reader(r_file)
            data = np.empty([100, 1], dtype=object)
            k = -1
            for row in file_reader:
                k = k + 1
                data[k] = row[0]
        self.dictionary = data
        self.Str_div()
        self.Table_build()
        self.Arr_handler()
        
    def Table_build(self):
        str_res_name = np.empty(0, dtype=object)
        str_res_value = np.empty(0, dtype=object)
        str_res_unit = np.empty(0, dtype=object)
        self.dict = pd.DataFrame({'Величина': str_res_name, 'Результат': str_res_value,
                             'Единица измерения': str_res_unit})
    def Str_div(self):
        str_arr = np.empty(0, dtype=object)
        for i in range(0, int(np.size(self.str.split('.')))):
            str_arr = np.concatenate((str_arr, self.str.split('.')[i].split(':')), axis=0)
        self.str_arr = str_arr
    def Arr_handler(self):
        k = -1
        t = 0
        M = int(np.size(self.str_arr))
        for i in range(0, M):
            punctuations = list(string.punctuation)
            words = [word for word in word_tokenize(self.str_arr[i]) if word not in punctuations]
            Col = TrigramCollocationFinder.from_words(words)
            N = np.shape(Col.nbest(TrigramAssocMeasures.likelihood_ratio, 10))[0]
            Col_Arr = np.empty([N, 1], dtype=object)
            for n in range(0, N):
                Col_Arr[n] = ' '.join(map(str, Col.nbest(TrigramAssocMeasures.likelihood_ratio, 10)[n]))
            if (np.size(Col_Arr) == 0):
                Col = BigramCollocationFinder.from_words(words)
                N = np.shape(Col.nbest(BigramAssocMeasures.likelihood_ratio, 10))[0]
                Col_Arr = np.empty([N, 1], dtype=object)
                for n in range(0, N):
                    Col_Arr[n] = ' '.join(map(str, Col.nbest(BigramAssocMeasures.likelihood_ratio, 10)[n]))
            str_col = np.empty([N, 3], dtype=object)
            for j in range(0, N):
                for s in range(0, np.size(word_tokenize(Col_Arr[j][0]))):
                    for one in (self.dictionary[:, 0]):
                        if (str(one) in word_tokenize(str(Col_Arr[j][0]))[s]) == True:
                            str_col[j, s] = word_tokenize(str(Col_Arr[j][0]))[s]
                if (str_col[j, 0] != None) & (str_col[j, 1] != None):
                    k = k + 1
                    self.dict.at[k, 'Величина'] = ' '.join(map(str, str_col[j, 0:2]))
                    self.dict.at[k, 'Результат'] = 'True'
                    self.dict.at[k, 'Единица измерения'] = 'Лог'
                if (str_col[j, :].all() != None):
                    self.dict.at[k, 'Величина'] = ' '.join(map(str, str_col[j, :]))
                    self.dict.at[k, 'Результат'] = 'True'
                    self.dict.at[k, 'Единица измерения'] = 'Лог'
                    for l in range(0, j):
                        if (str_col[j, 0] == str_col[l, 1] and str_col[j, 1] == str_col[l, 2] and str_col[l, :].any != None):
                            k = k - 1

                            self.dict.at[k, 'Величина'] = ' '.join(map(str, str_col[l, :])) + ' ' + str(str_col[j, 2])
                            self.dict.at[k, 'Результат'] = 'True'
                            self.dict.at[k, 'Единица измерения'] = 'Лог'
            if (t != k):
                self.Value_finder(i, t)
            t = k
        print(self.dict)
    def Value_finder(self, i, t):
        text = str(self.str_arr[i])
        words = text.split(' ')
        index_name = np.zeros(np.size(self.dict))
        delta_r = np.ones(np.size(self.dict)) * 100
        for one in words:
            if ('I' in one) == True or any(chr.isdigit() for chr in one) == True:
                index_val = text.rindex(one)
                for j in range(t + 1, int(np.shape(self.dict)[0])):
                    index_name[j] = int(text.rindex(self.dict.at[j, 'Величина']) + len(self.dict.at[j, 'Величина']))
                    if index_val > index_name[j]:
                        delta_r[j] = index_val - index_name[j]
                if ('I' in one) == True:
                    self.dict.at[list(delta_r).index(min(delta_r[:])), 'Результат'] = one
                    self.dict.at[list(delta_r).index(min(delta_r[:])), 'Единица измерения'] = 'Стадия/степень'
                if any(chr.isdigit() for chr in one) == True:
                    self.dict.at[list(delta_r).index(min(delta_r[:])), 'Результат'] = one
                    self.dict.at[list(delta_r).index(min(delta_r[:])), 'Единица измерения'] = 'Ед.'
