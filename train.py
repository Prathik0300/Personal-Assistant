import json
import pickle

Intents = json.loads(open("intents.json").read())
doc = {}
for intent in Intents['intents']:
    tag = intent['tag']
    for word in intent['patterns']:
        doc[word.lower()]=tag

pickle.dump(doc,open("patterns.pkl","wb"))


    
