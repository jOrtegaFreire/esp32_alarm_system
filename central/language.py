import json

def load_language(lang):
    with open(lang+'.json','r') as f:
        language=json.load(f)
    
    return language