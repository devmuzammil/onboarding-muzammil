import json

def save_expenses(expenses):
    with open('expenses.json','w') as file:
        json.dump(expenses,file,indent=4)

def load_expenses():
    try:
        with open('expenses.json','r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []