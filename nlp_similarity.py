import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import nltk
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import sent_tokenize, word_tokenize

nltk.download('stopwords')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_lg')


datasets=['dataset.csv',
            'symptom_Description.csv',
            'symptom_precaution.csv',
            'Symptom-severity.csv']
path='./dataset/'
df_symptoms = pd.read_csv(path+datasets[0])
df_diseases = pd.read_csv(path+datasets[1])
df_precautions = pd.read_csv(path+datasets[2])
df_symps_weights = pd.read_csv(path+datasets[3]) # Weights for symptoms, or labelEncoder, NOt that Relevant for NLP... so far


df_symptoms=df_symptoms.fillna("")
for col in df_symptoms.drop('Disease', axis=1).columns:
    df_symptoms[col]=df_symptoms[col].str.replace("_"," ")

# MERGE 3 Datasets in one DF. Maintain repetition of diseases to increase match
## Create a relation between the 3 main datasets, which is Disease and symptom
df_complete = pd.DataFrame()
df_complete = pd.merge(df_symptoms,df_diseases, on='Disease')
df_complete = pd.merge(df_complete,df_precautions, on='Disease')


df_complete['Precaution_1']=df_complete['Precaution_1'].astype(str)
df_complete['Precaution_2']=df_complete['Precaution_2'].astype(str)
df_complete['Precaution_3']=df_complete['Precaution_3'].astype(str)
df_complete['Precaution_4']=df_complete['Precaution_4'].astype(str)


list_symptoms=list({'abdominal pain',
 'abnormal menstruation',
 'acidity',
 'acute liver failure',
 'altered sensorium',
 'anxiety',
 'back pain',
 'belly pain',
 'blackheads',
 'bladder discomfort',
 'blister',
 'blood in sputum',
 'bloody stool',
 'blurred and distorted vision',
 'breathlessness',
 'brittle nails',
 'bruising',
 'burning micturition',
 'chest pain',
 'chills',
 'cold hands and feets',
 'coma',
 'congestion',
 'constipation',
 'continuous feel of urine',
 'continuous sneezing',
 'cough',
 'cramps',
 'dark urine',
 'dehydration',
 'depression',
 'diarrhoea',
 'dischromic  patches',
 'distention of abdomen',
 'dizziness',
 'drying and tingling lips',
 'enlarged thyroid',
 'excessive hunger',
 'extra marital contacts',
 'family history',
 'fast heart rate',
 'fatigue',
 'fluid overload',
 'foul smell of urine',
 'headache',
 'high fever',
 'hip joint pain',
 'history of alcohol consumption',
 'increased appetite',
 'indigestion',
 'inflammatory nails',
 'internal itching',
 'irregular sugar level',
 'irritability',
 'irritation in anus',
 'itching',
 'joint pain',
 'knee pain',
 'lack of concentration',
 'lethargy',
 'loss of appetite',
 'loss of balance',
 'loss of smell',
 'malaise',
 'mild fever',
 'mood swings',
 'movement stiffness',
 'mucoid sputum',
 'muscle pain',
 'muscle wasting',
 'muscle weakness',
 'nausea',
 'neck pain',
 'nodal skin eruptions',
 'obesity',
 'pain behind the eyes',
 'pain during bowel movements',
 'pain in anal region',
 'painful walking',
 'palpitations',
 'passage of gases',
 'patches in throat',
 'phlegm',
 'polyuria',
 'prominent veins on calf',
 'puffy face and eyes',
 'pus filled pimples',
 'receiving blood transfusion',
 'receiving unsterile injections',
 'red sore around nose',
 'red spots over body',
 'redness of eyes',
 'restlessness',
 'runny nose',
 'rusty sputum',
 'scurring',
 'shivering',
 'silver like dusting',
 'sinus pressure',
 'skin peeling',
 'skin rash',
 'slurred speech',
 'small dents in nails',
 'spinning movements',
 'spotting  urination',
 'stiff neck',
 'stomach bleeding',
 'stomach pain',
 'sunken eyes',
 'sweating',
 'swelled lymph nodes',
 'swelling joints',
 'swelling of stomach',
 'swollen blood vessels',
 'swollen extremeties',
 'swollen legs',
 'throat irritation',
 'toxic look (typhos)',
 'ulcers on tongue',
 'unsteadiness',
 'visual disturbances',
 'vomiting',
 'watering from eyes',
 'weakness in limbs',
 'weakness of one body side',
 'weight gain',
 'weight loss',
 'yellow crust ooze',
 'yellow urine',
 'yellowing of eyes',
 'yellowish skin'})

def preprocess(text):
    doc = nlp(text)
    lemmatized = [lemmatizer.lemmatize(token.text) for token in doc]
    clean_text = ' '.join([word.lower() for word in lemmatized if word.lower() not in stop_words and word.isalpha()])
    return clean_text

def cleaning_process(df,syms='symptoms',des='description'):
    # I forgot the reason behind syms and des
    df = df.drop_duplicates()
    df = df.fillna("")
    df['processed_symptoms'] = df[syms].apply(preprocess)
    df['processed_description'] = df[des].apply(preprocess)
    return df



# Obtaining column names for 17 symptoms columns
sym_cols=[]
for i in range(1,18):
    sym_cols.append('Symptom_'+str(i))    
df_complete['Symptoms_All'] = df_complete[sym_cols].apply(lambda row: ', '.join(row), axis=1)


#Obtaining columns for precautions, merge last 3 into one
prec_cols=[]
for i in range(2,4):
    prec_cols.append('Precaution_'+str(i))    
df_complete['Precautions'] = df_complete[prec_cols].apply(lambda row: ', '.join(row), axis=1)




columns_of_interest=['Disease','Symptoms_All','Description',"Precaution_1",'Precautions'] #for training
_df=cleaning_process(df_complete[columns_of_interest],'Symptoms_All','Description')









    



#################################
# NLP DETECTION
#################################


def clean_text(text):
    text = text.replace('\n','. ')#.replace('','').replace('','').replace('','')
#     text = text.replace(',',' ').replace('!','').replace('?','')
    return text

def remove_punct(text, lower=False):
    if(type(text)==str):
        text = text.replace('\n','. ')#.replace('','').replace('','').replace('','')
        text = text.replace(',',' ').replace('!','').replace('?',' ')
        text = text.replace('.',' ').replace('#','').replace('$',' ')
        text = text.replace('^',' ').replace('&','and').replace(';',' ')
        text = text.replace('  ',' ')
        return text
    elif(type(text)==list):
        _words=[]
        for w in text:
            if w.isalnum():
                _words.append(w if not lower else w.lower())
#         print('remove_punct',len(_words))
        return _words

def get_sentences(text):
    return sent_tokenize(text)

def get_tokens(text):
    words =[]
    for w in word_tokenize(text):
        if w.isalnum():
            words.append(w)
    return words
    

def remove_stopwords(words):
    just_words=[]
    for word in words:
        if word.lower() not in stop_words:
            just_words.append(word)
    return just_words
    
    
def lemmatize(text):
    record_lemmatized = [lemmatizer.lemmatize(token) for token in text]
    return record_lemmatized
    
    
def list_to_string(ls):
    return (" ".join(ls)).strip()
    
# clean words: boooook
# Remove non stop words of 2 letters

def preprocess_text_ap1(x):
       # tokenize everything, remove stop words, lower all, remove punctutation
    # set tokens each description
    dataset_tokens= get_tokens(x)
    # remove stopwords
    dataset_nostopwords= remove_stopwords(dataset_tokens)
    # remove punctuation
    dataset_main_words= remove_punct(dataset_nostopwords, lower=False)
    # Lower all
    dataset_main_words_lower=[x.lower() for x in dataset_main_words]# estaba comentado
    # Back to string
    dataset_clean_text =  list_to_string(dataset_main_words_lower)
    return dataset_clean_text






#################################
# CREATE VECTORS
#################################


# processed_symptoms	processed_description
import os
import time
import pickle

DOCS_DATABASE_ROOT = "./models/DISEASES_v2"

dataset_docs=[]
tic=time.time()
if not os.path.exists(DOCS_DATABASE_ROOT):
    print("This DISEASES database has not been processed, creating NLP docs...")
    os.makedirs(DOCS_DATABASE_ROOT)
    # To avoid too much disk space
    
    dataset_docs = [nlp(record) for record in _df['processed_description'].tolist()]
    # save dataset_docs in pickle
    with open(DOCS_DATABASE_ROOT+'/dataset_disease_docs.pkl', 'wb') as f:
        pickle.dump(dataset_docs, f)
    print(f"{len(dataset_docs)} docs . Took {(time.time()-tic)} secs to process") # 89 docs on 26.4 secs

else:
    with open(DOCS_DATABASE_ROOT+'/dataset_disease_docs.pkl', 'rb') as f:
        dataset_docs = pickle.load(f)
    print(f"{len(dataset_docs)} docs . Took {(time.time()-tic)} secs to load")

    
    
# SYMPTOMS
DOCS_DATABASE_ROOT_SYMS = "./models/DISEASES_SYMPS_v2"

dataset_docs=[]
if not os.path.exists(DOCS_DATABASE_ROOT_SYMS):
    print("This SYMPTOMS database has not been processed, creating NLP docs...")
    os.makedirs(DOCS_DATABASE_ROOT_SYMS)
    # To avoid too much disk space
    tic=time.time()
    dataset__syms_docs = [nlp(record) for record in _df['processed_symptoms'].tolist()]
    print(f"{len(dataset__syms_docs)} docs . Took {(time.time()-tic)} secs to process") # 89 docs on 26.4 secs
    # save dataset_docs in pickle
    with open(DOCS_DATABASE_ROOT_SYMS+'/dataset_symptoms_docs.pkl', 'wb') as f:
        pickle.dump(dataset__syms_docs, f)
else:
    with open(DOCS_DATABASE_ROOT_SYMS+'/dataset_symptoms_docs.pkl', 'rb') as f:
        dataset__syms_docs = pickle.load(f)
    print(f"{len(dataset__syms_docs)} docs . Took {(time.time()-tic)} secs to load")

    
    
#USER INPUT
def preprocess_user_input(user_input):
    return preprocess(user_input)


def find_similar_disease(_synopsis, dataset_docs="disease"):
    if dataset_docs=="symptoms":
        dataset_docs = dataset__syms_docs
    else:
        dataset_docs = dataset_docs

    summary_raw=_synopsis 
    summary=preprocess_user_input(summary_raw)
    summary_doc = nlp(summary)
    similarity_scores = [summary_doc.similarity(doc) for doc in dataset_docs]
    most_similar_index = similarity_scores.index(max(similarity_scores))
  
    df_match = _df.iloc[most_similar_index]#[df['']]

    # get symptoms on text || Firt attempt was with spacy entities.
    found_symptoms=[]
    for _sym in list_symptoms:
        if(_sym  in _synopsis):
            found_symptoms.append(_sym)



    # DF_MATCH:Disease,Symptoms_All,Description,processed_symptoms,processed_description
    txt_disease_details={
        'disease': df_match['Disease'],
        'description': df_match['Description'],
        'treatment': df_match['Precaution_1'],
        'treatments': df_match['Precautions'],
        'symptoms': (", ".join(found_symptoms))[:-1]
    }


    return txt_disease_details #df_match #most_similar_record.text








#################################
# TEST
#################################

# count=0
# for k,v_text in testes.items():
#     print("====================")
#     _ct= find_similar_disease(v_text,dataset__syms_docs) #HERE YOU CALL  YOUR FUNCTION TO PROCESS v_text
#     r= "✅" if _ct['Disease'] == k.strip() else "❌"
#     if("✅"==r):
#         count+=1
#     print(r , end=" ")
#     print(f"Predicted: {_ct['Disease']}, Original: {k},  \n\tSentence: {v_text}")
# print(f"Total {count}/{len(testes)}")

#by symptoms no lemma  :Total 13/41
# By description: 8/41
# By symproms, but with lemma 13/28 BUT! some good wrong predictions

"""====================
❌ Predicted: Drug Reaction, Original: Acne,  
	Sentence: Pus-filled pimples have been appearing on my skin, causing discomfort and frustration.
====================
❌ Predicted: Acne, Original: Fungal infection,  
	Sentence: My skin has been itchy and flaky with a reddish rash that doesn't seem to heal.
====================
❌ Predicted: Urinary tract infection, Original: Urinary tract infection (UTI),  
	Sentence: I've had a burning sensation when I urinate, and I feel the urge to go more often than usual.
====================
❌ Predicted: Hepatitis E, Original: Hepatitis D,  
	Sentence: I've had jaundice, fatigue, and joint pain recently, even though I already had hepatitis B.
====================
❌ Predicted: Hepatitis C, Original: Hepatitis B,  
	Sentence: I've been feeling very tired, my urine is dark, and there's a yellowish tinge to my eyes and skin.
====================
❌ Predicted: (vertigo) Paroymsal  Positional Vertigo, Original: Drug Reaction,  
	Sentence: After taking that medication, I developed a rash, swelling, and felt dizzy.
====================
✅ Predicted: Paralysis (brain hemorrhage), Original: Paralysis (brain hemorrhage),  
	Sentence: Half of my body suddenly became weak, and I couldn't move my right arm or leg.
====================
✅ Predicted: Chicken pox, Original: Chicken pox,  
	Sentence: I've broken out in itchy blisters all over my body, and I had a fever before the rash appeared.
====================
✅ Predicted: Dengue, Original: Dengue,  
	Sentence: I'm feeling sudden high fever, severe headaches, and pain behind my eyes, along with joint and muscle pain.
====================
✅ Predicted: Typhoid, Original: Typhoid,  
	Sentence: I've been suffering from a persistent fever, stomach pain, headache, and I noticed a rash on my abdomen.
====================
❌ Predicted: Hypothyroidism, Original: Hepatitis A,  
	Sentence: I've lost my appetite, feel nauseous, and my liver area hurts; plus, I've noticed a yellowing of my eyes.
====================
❌ Predicted: Urinary tract infection, Original: Hepatitis C,  
	Sentence: I'm feeling a general sense of fatigue, my stomach is upset, and the doctor said my liver enzymes are elevated.
====================
❌ Predicted: Typhoid, Original: Hepatitis E,  
	Sentence: I've noticed jaundice, feel fatigued, and have a reduced appetite along with mild fever.
====================
❌ Predicted: Chronic cholestasis, Original: Alcoholic hepatitis,  
	Sentence: After years of heavy drinking, I've been feeling nauseous, have abdominal pain, and my eyes and skin are turning yellow.
====================
✅ Predicted: Tuberculosis, Original: Tuberculosis,  
	Sentence: I've had a persistent cough for weeks, sometimes coughing up blood, accompanied by weight loss, night sweats, and fatigue.
====================
✅ Predicted: Common Cold, Original: Common Cold,  
	Sentence: I've got a runny nose, sneezing, a mild sore throat, and a cough that just started.
====================
✅ Predicted: Pneumonia, Original: Pneumonia,  
	Sentence: I've been feeling short of breath, with a high fever and a cough that brings up thick, colored phlegm.
====================
❌ Predicted: Varicose veins, Original: Dimorphic hemorrhoids (piles),  
	Sentence: I've noticed painful swollen veins in my rectal area, and sometimes there's blood when I wipe.
====================
✅ Predicted: Heart attack, Original: Heart attack,  
	Sentence: I suddenly felt a crushing pain in my chest that radiated to my arm and jaw, accompanied by shortness of breath.
====================
✅ Predicted: Varicose veins, Original: Varicose veins,  
	Sentence: The veins in my legs have become bulgy, bluish, and often cause a dull ache.
====================
✅ Predicted: Hypothyroidism, Original: Hypothyroidism,  
	Sentence: I've been feeling constantly tired, gaining weight, and my skin has turned dry and cold.
====================
✅ Predicted: Hyperthyroidism, Original: Hyperthyroidism,  
	Sentence: I've lost weight without trying, my heart rate has increased, and I feel jittery and hot all the time.
====================
❌ Predicted: Urinary tract infection, Original: Hypoglycemia,  
	Sentence: I suddenly felt shaky, sweaty, and had a pounding heartbeat, and needed to eat something sweet immediately.
====================
❌ Predicted: Arthritis, Original: Osteoarthritis,  
	Sentence: The joints in my hands and knees have become painful and stiff, especially when I wake up.
====================
❌ Predicted: Impetigo, Original: Arthritis,  
	Sentence: My joints are swollen, red, and warm to the touch, and they ache constantly.
====================
❌ Predicted: Impetigo, Original: Psoriasis,  
	Sentence: There are red, itchy patches covered with silvery scales on my elbows and knees.
====================
✅ Predicted: Impetigo, Original: Impetigo,  
	Sentence: I've developed red sores around my nose and noticed yellow crust ooze, suggesting possible impetigo.
====================
✅ Predicted: Migraine, Original: Migraine,  
	Sentence: I've been experiencing severe headaches, often accompanied by visual disturbances and sensitivity to light.
Total 13/28"""