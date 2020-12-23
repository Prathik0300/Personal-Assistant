import pickle
import json
from collections import defaultdict

l = [0]
pickle.dump(l,open("C:\college\Github_improvement\Search\Trained Data\personalMail.pkl","wb"))
pickle.dump(l,open("C:\college\Github_improvement\Search\Trained Data\workMail.pkl","wb"))


Intents = json.loads(open("intents.json").read())
doc = {}
for intent in Intents['intents']:
    tag = intent['tag']
    for word in intent['patterns']:
        doc[word.lower()]=tag

pickle.dump(doc,open("C:\college\Github_improvement\Search\Trained Data\patterns.pkl","wb"))

assistant = defaultdict(list)
assistant['name'].append("I am Iris, your personal assistant")
assistant['age'].append("I am still pretty new")
assistant['age'].append("I am Young but not baby young")

pickle.dump(assistant,open("C:\college\Github_improvement\Search\Trained Data\SelfInfo.pkl","wb"))


