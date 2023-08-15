import spacy
import nltk




def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_user_details(txt_user_data):
    def calculate_bmi(weight, height):
        """Calculate BMI (kg) and (m)"""
        return weight / (height ** 2)
    def feet_to_meters(feet):
        return feet * 0.3048
    def pounds_to_kilograms(pounds):
        return pounds * 0.453592



    # txt_user_data = "My name is John, male, I have 18 years old, and I am 1.65 meters, weight 100 pounds."

    # Extract entities from the text
    entities = extract_entities(txt_user_data)

    # Initialize an empty dictionary to store user details
    user_details = {
        "name": None,
        "age": None,
        "height": None,
        "weight": None,
        "bmi":None
    }

    print(entities)
    # Iterate through extracted entities to find user details
    for entity, label in entities:
        if label == "PERSON":
            user_details["name"] = entity
        elif label == "DATE":
            if ("years" in entity or "y.o." in entity):
                user_details["age"] = int(entity.split()[0])
        elif (label == "QUANTITY"):
            if ("feet" in entity or "ft." in entity):
                user_details["height"] = feet_to_meters(float(entity.split()[0]))
            elif ("meters" in entity or "mts." in entity):
                user_details["height"] = float(entity.split()[0]) 
            elif ("centimeter" in entity or "cm." in entity):
                print("Is in centimeters",entity)
                print((float(entity.split()[0]))/100, "meters")
                user_details["height"] = (float(entity.split()[0]))/100
            elif any(unit in entity for unit in ["kg", "pounds", "kilo"]):
                if "pounds" in entity:
                    user_details["weight"] = pounds_to_kilograms(float(entity.split()[0]))
                elif any(unit in entity for unit in ["kg", "kilo"]):
                    user_details["weight"] = float(entity.split()[0])
            elif(label == "CARDINAL"):
                # If just caught a number without extra context.... 
                # Add it to all empty values? measure and guess its variable?
                for k,v in user_details.items():
                    if(user_details[k]==None):
                        (float(entity.split()[0]))/100
                        x=float(entity.split()[0])
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
