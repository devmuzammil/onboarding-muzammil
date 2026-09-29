from models import create_expense
expenses=[]

expense=create_expense(100,'food','2023-06-01','lunch')
expenses.append(expense)
print(expenses)