
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

_synopsis="David here a 41 year old waiting in at 185 pounds and touring 1.81 meters above ground. A Half of my body suddenly became weak and I couldn't move my right arm or leg."
# get symptoms on text || Firt attempt was with spacy entities.
found_symptoms=[]
for _sym in list_symptoms:
    print(_sym)
    if(_sym  in _synopsis):
        found_symptoms.append(_sym.capitalize())
print(found_symptoms)

user={
        'disease': "df_match['Disease']",
        'description': "df_match['Description']",
        'treatment': "df_match['Precaution_1']",
        'treatments':" df_match['Precautions']",
        'symptoms': ", ".join(found_symptoms)
    }

if(len(user['symptoms'])!=0):
    print("THere are symptoms")
else:
    print("There are  NO symptoms")