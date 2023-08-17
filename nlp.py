import spacy
import nltk
import re


nlp_entities = spacy.load('en_core_web_sm') 

def extract_entities(text, lan_model="en_core_web_sm"):
    global nlp_entities
    if(lan_model!="en_core_web_sm"):
        nlp_entities = spacy.load(lan_model)
    doc = nlp_entities(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_user_details(txt_user_data):
    def calculate_bmi(weight, height):
        """Calculate BMI (kg) and (m)"""
        return float(weight / (height ** 2))
    def feet_to_meters(feet):
        return feet * 0.3048
    def pounds_to_kilograms(pounds):
        return pounds * 0.453592
    # Extract entities from the text
    entities = extract_entities(txt_user_data, "en_core_web_lg")

    # Initialize an empty dictionary to store user details
    user_details = {
        "name": "",
        "age": 0,
        "height": 0,
        "weight": 0,
        "bmi":0
    }

    print(entities)
    # Iterate through extracted entities to find user details
    for entity, label in entities:
        print(f"Entity:{entity}, {label}")
        entity_value=re.sub(r'[^0-9.]', '',entity.split()[0])
        if(entity_value==""):
            entity_value=0
        if label == "PERSON":
            user_details["name"] = entity
        elif label == "DATE":
            if ( entity in ["years","y.o.", "year", "yo."]):
                user_details["age"] = int(entity_value)
        elif (label == "QUANTITY"):
            if ("feet" in entity or "ft." in entity):
                user_details["height"] = feet_to_meters(float(entity_value))
            elif (entity in ["meters", "mts.", "meter"]):
                user_details["height"] = float(entity_value)
            elif (entity in ["centimeter","cm." , "centimeters", 'cms.']):
                print("Is in centimeters",entity)
                print((float(entity_value))/100, "meters")
                user_details["height"] = (float(entity_value))/100
            elif any(unit in entity for unit in ["kg","kg.", "pounds", "kilo", 'kilogram','kilograms']):
                if "pounds" in entity:
                    user_details["weight"] = pounds_to_kilograms(float(entity_value))
                elif any(unit in entity for unit in ["kg", "kilo"]):
                    user_details["weight"] = float(entity_value)
        elif(label == "CARDINAL"):
            # If just caught a number without extra context.... 
            # Add it to all empty values? measure and guess its variable?
            for k,v in user_details.items():
                if(user_details[k]==""):
                    (float(entity_value))/100
                    x=float(entity_value)
                    if (k == 'height' and x > 2):
                        user_details[k] = x/100 
                    elif (k == 'weight' and x > 160): # this is consideration of 160 and above as pounds
                        user_details[k] = pounds_to_kilograms(x)
                    else:
                        user_details[k] = x
    #Process bodymass
    if user_details["height"] and user_details["weight"]:
        user_details["bmi"] = calculate_bmi(user_details["weight"], user_details["height"])

    print("User Details:", user_details)
    return user_details



##########################################
############# Text Splitter ##############
##########################################


def split_text_content(full_text):
    """split_text_content, will detect wich sentence contain more semantic information related to user details, and use it to split the information"""
    
    # Split full_text in sentences
    sentences = nltk.sent_tokenize(full_text)

    # dictionary to hold the index of the sentence and keep a counter for matches
    sentence_index = {}

    for index,sentence in enumerate(sentences):
        entities = extract_entities(sentence, "en_core_web_sm")
        counter=0
        for entity, label in entities:
            if label  in ["PERSON","DATE","QUANTITY","CARDINAL"]:
                counter+=1
        sentence_index[index] = counter
    
    # Detect the sentence_index with greater counter
    max_index = max(sentence_index, key=sentence_index.get)
    user_text = sentences[max_index].strip()
    #remove user_text form original full_text
    symptom_text = full_text.replace(user_text,"").strip()

    print("user_text:",user_text)
    print("symptoms_text:",symptom_text)

    return user_text, symptom_text