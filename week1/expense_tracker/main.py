from models import create_expense
expenses=[]

def add_expense():
    amount=float(input('Amount = '))
    category=input('Category = ')
    date=input('Date = ')
    note=input('Note = ')

    expense=create_expense(amount,category,date,note)
    expenses.append(expense)

    print('Expense Added')

def list_expenses():
    for expense in expenses:
        print(expense)

def summary():
    total = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category not in total:
            total[category] = 0

        total[category] += amount

    print(total)

add_expense()
add_expense()

list_expenses()
summary()