#Сделана работа по нахождению пола, возраста, айди пациента, а также первого факта, который попадается по пути поиска. Я продолжу продумывать, как можно реализовать нахождение всех
#фактов, скорее всего, воспользуюсь поиском по айди

import pandas,spacy
#open file
recs = pandas.read_pickle('records.pkl')
print(recs.head)

Impression = recs[recs["Статус"] == "ПРЕДСТАВЛЕНИЕ О БОЛЬНОМ"]
Info = Impression["Данные"]
Id = Impression["patient_ID"]

nlp = spacy.load("ru_core_news_lg")

Impression = pandas.DataFrame.to_string(Impression)
Info = pandas.Series.to_string(Info)
Id = pandas.Series.to_string(Id)

document = nlp(Impression)
doc_ID = nlp(Id)
doc_Info = nlp(Info)

#Массив айди с уникальными номерами
uniq = []
for token in doc_ID:
    if token.text in uniq:
        continue
    elif (token.pos_!= "NUM") & (token.dep_ != "dep")&(token.pos_!= "ADJ")&(token.pos_!= "PUNCT"):
        uniq.append(token.text)

def conversely(s):
    s = s.split()
    s.reverse()
    s2 = ' '.join(s)
    return s2

class Parser_:
    def __init__(self,original_record):
        self.contain = original_record
    def conversely(self,s):
        s = s.split()
        s.reverse()
        s2 = ' '.join(s)
        return s2
        
    def parce(self):
        num = 0
        Patient_dict = {}
        new_dict={}
        meaning = str()
        keyword = str()

        for token in self.contain:
            if token.text ==":":
                keyword = str()
                meaning = str()
                a = token.i
                b = token.i
                while self.contain[a].pos_ != "SPACE" or self.contain[a].text == "/n":
                    if (self.contain[a].text != ":") & (self.contain[a].pos_ != "NUM"):
                        keyword +=str(self.contain[a].text) + ' '
                    a = a-1
                while self.contain[b].pos_ != "SPACE" or self.contain[b].text == "/n":
                    if (self.contain[b].text != ":"):
                        meaning += str(self.contain[b].text) + ' '
                    b = b+1
                    
            if token.text == "Пациент" or token.text == "Пациентка" or token.text == "Мальчик" or token.text == "Девочка":
                if self.contain[token.i+1].pos_ == "NUM":
                    if token.text == "Пациент" or token.text == "Мальчик":
                        new_dict["Пол"] = "Мужской"
                        new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
                        new_dict['ID'] = uniq[num]
                    else:
                        new_dict["Пол"] = "Женский"
                        new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
                        new_dict['ID'] = uniq[num]
                    num+=1
                    new_dict[str(conversely(keyword))] = str(meaning)
                    Patient_dict['Пациент ' + '' + str(num)] = new_dict
                    new_dict={}
        return Patient_dict
                                           

Impression1 = Parser_(document)
New_dict = Parser_.parce(Impression1)
print(New_dict['Пациент 4']['Возраст'])
print(New_dict)




# new_dict = {}
# Patient_dict ={}
# num = 0
# meaning = str()
# keyword = str()
# for token in document:
#     if token.text == ":":
#         keyword = str()
#         meaning = str()
#         a = token.i
#         b = token.i
#         while document[a].pos_ != "SPACE" or document[a].text == "/n":
#             if (document[a].text != ":") & (document[a].pos_ != "NUM"):
#                 keyword += str(document[a].text) + ' '
#             a=a-1
#         while document[b].pos_ != "SPACE" or document[b].text == "/n":
#             if (document[b].text != ":"):
#                 meaning += str(document[b].text)
#             b=b+1
#     if token.text == "Пациент" or token.text == "Пациентка" or token.text == "Мальчик" or token.text == "Девочка":
#         if document[token.i+1].pos_ == "NUM":
#             if token.text =="Пациент" or token.text =="Мальчик":
#                 new_dict["Пол"] = "Мужской"
#                 new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
#                 new_dict['ID'] = uniq[num]
#             else:
#                 new_dict["Пол"] = "Женский"
#                 new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
#                 new_dict['ID'] = uniq[num] 
#             num +=1                           
#             new_dict[conversely(str(keyword))] = str(meaning)
#             Patient_dict['Пациент ' + '' + str(num)] = new_dict
#             new_dict = {}


# new_dict = {}
# Patient_dict ={}
# num = 0

# for token in document:
#     if token.text == "Пациент" or token.text == "Пациентка" or token.text == "Мальчик" or token.text == "Девочка":
#         if document[token.i+1].pos_ == "NUM":
#             if token.text =="Пациент" or token.text =="Мальчик":
#                 new_dict["Пол"] = "Мужской"
#                 new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
#                 new_dict['ID'] = uniq[num]
#             else:
#                 new_dict["Пол"] = "Женский"
#                 new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
#                 new_dict['ID'] = uniq[num] 
#             num +=1                           
#         c = token.i
#         while document[c].text != ":":
#             c += 1
#             if token.text == ":":
#                 keyword = str()
#                 meaning = str()
#                 a = c
#                 b=c
#                 while document[a].pos_ != "SPACE" or document[a].text == "/n":
#                     if (document[a].text != ":") & (document[a].pos_ != "NUM"):
#                         keyword += str(document[a].text) + ' '
#                     a=a-1
#                 while document[b].pos_ != "SPACE" or document[b].text == "/n":
#                     if (document[b].text != ":"):
#                         meaning += str(document[b].text)
#                     b=b+1
#             new_dict[conversely(str(keyword))] = str(meaning)
#             Patient_dict['Пациент ' + '' + str(num)] = new_dict
#             new_dict = {}


# print(Patient_dict)
# print(Patient_dict["Пациент 1"]["Возраст"])




# Patient_dict["Пациент 1"]["ROST"] = 179


# document1 = document[1:200]
# document2 = doc_Info[1:200]
# print(document1)
# print(document2)
# for token in document2:
#     print(token.text,token.dep_,token.pos_)
 
# new_dict={}    
# Patient_dict={}
# for token in document:
#     keyword = str()
#     meaning = str()
#     if token.text == ":" :
#         a = token.i
#         b = token.i
#         while document[a].pos_ != "SPACE" or document[a].text == "/n":
#             if (document[a].text != ":") & (document[a].pos_ != "NUM"):
#                 keyword += str(document2[a].text) + ' '
#             a=a-1
#         while document[b].pos_ != "SPACE" or document[b].text == "/n":
#             meaning += str(document[b].text) 
#             b=b+1
#         new_dict[conversely(str(keyword))] = str(meaning)
        



# print(new_dict)

#frst = pandas.DataFrame.first(recs)
#print(recs["Статус"])
#print(recs.iloc[0:2]) #Series - type of this
#print(recs.loc[119]) #непосредственно та, как отменчена
#Diag_Staz = recs[recs["Статус"] == 'ДИАГНОЗ СТАЦИОНАРНЫЙ']
#print(Diag_Staz,type(Diag_Staz))
#print(type(Id),Id)
#print(type(Impression))
#print(Impression.iloc[0:2])
#print(Impression.loc[155]) #непосредственно та, как отменчена
#print(Impression,type(Impression))
#print(Impression.iloc[50:60]) #Series - type of this
#print(Impression.loc[155])
#npl
#nlp = spacy.blank('ru')
#doc= nlp("Этот выбор мы делаем уже в детстве, когда выбираем друзей, учимся строить отношения с ровесниками, играть. Но большинство важнейших решений, определяющих жизненный путь, мы всё-таки принимаем в юности. Как считают учёные, вторая половина второго десятилетия жизни – самый ответственный период. Именно в это время человек, как правило, выбирает самое главное и на всю жизнь: ближайшего друга, круг основных интересов, профессию.")
#Diag_Staz = pandas.DataFrame.to_string(Diag_Staz)

# print(document1[15].text,document[0].dep_,document1[0].pos_)
# temp =str()
# temp3 = 0
# for token in document1:  
#     if token.text == "БОЛЬНОМ":
#         for token1 in document1[token.i:len(document1)]:
#             temp2=uniq[temp3]
#             while token1.text != temp2:
                
#             if token1.text in uniq:
#                 temp2 = token1.text
#                 if token1.text!=temp2:
#                     break
#             elif (token1.pos_ != "SPACE") & (token1.text!="БОЛЬНОМ")&(token1.text!="ПРЕДСТАВЛЕНИЕ")&(token1.text!="О"):
#                 temp += str(token1.text) + ' '                       
#         num+=1
#     new_dict['Patient ' + 'number ' + str(num)] = temp 
   
                
# print(new_dict)   



# new_dict = {}
# Patient_dict ={}
# num = 0


# for token in document:
#     if token.text == "Пациент" or token.text == "Пациентка" or token.text == "Мальчик" or token.text == "Девочка":
#         if document[token.i+1].pos_ == "NUM":
#             if token.text =="Пациент" or token.text =="Мальчик":
#                 new_dict["Пол"] = "Мужской"
#                 new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
#                 new_dict['ID'] = uniq[num]
#             else:
#                 new_dict["Пол"] = "Женский"
#                 new_dict['Возраст'] = str(document[token.i+1].text) + ' ' + str(document[token.i+2].text)
#                 new_dict['ID'] = uniq[num]                              
#             num +=1
#             Patient_dict['Пациент ' + '' + str(num)] = new_dict
#             new_dict = {}



# for ent in document1.ents:
#     print(ent.text)

# print("Index:   ", [token.i for token in document])
# print("Text:    ", [token.text for token in document])

# print("is_alpha:", [token.is_alpha for token in document])
# print("is_punct:", [token.is_punct for token in document])
# print("like_num:", [token.like_num for token in document])
#x = pandas.DataFrame.to_csv(recs)
#y = pandas.DataFrame.to_dict(recs)

#, token.lemma_, token.pos_, token.is_stop



#print(type(recs),recs)
#print(type(y))
#print(y.get('Данные'))


#words = nlp(x)
#token = y['Статус']
#print((token.get('ЖАЛОБЫ')))



#print("Index:   ", [token.i for token in y])
#print("Text:    ", [token.text for token in y])

#print(type(recs))
#print(recs[119])

#print(type(x))
#print(x[1:530])



# x = {"Vozrast":3,"Rost" :120,"Pol":"W"}
# y = {"Vozrast":17,"Rost" :179,"Pol":"M"}
# z = {"Vozrast":44,"Rost" :159,"Pol":"W"}

# aboba = dict(Patient1=x)
# aboba["Patient2"] =  (y)
# print(type(aboba),aboba)

#new = []




        