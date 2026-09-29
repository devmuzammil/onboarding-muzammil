from models import create_expense
from storage import save_expenses, load_expenses

import argparse
import csv
from datetime import datetime


expenses = load_expenses()


def add_expense():
    try:
        amount = float(input("Amount = "))

        if amount < 0:
            print("Invalid amount: amount cannot be negative.")
            return

        category = input("Category = ")
        date = input("Date (YYYY-MM-DD) = ")

        # Check if date is valid
        datetime.strptime(date, "%Y-%m-%d")

        note = input("Note = ")

        expense = create_expense(
            amount,
            category,
            date,
            note
        )

        expenses.append(expense)
        save_expenses(expenses)

        print("Expense Added")

    except ValueError:
        print("Invalid input. Please enter a valid amount and date (YYYY-MM-DD).")


def list_expenses():
    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        print(
            f"{expense['amount']} - "
            f"{expense['category']} - "
            f"{expense['date']} - "
            f"{expense['note']}"
        )


def summary():
    total = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category not in total:
            total[category] = 0

        total[category] += amount

    if not total:
        print("No expenses found.")
        return

    for category, amount in total.items():
        print(f"{category}: {amount}")


def export_csv():
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "amount",
            "category",
            "date",
            "note"
        ])

        for expense in expenses:
            writer.writerow([
                expense["amount"],
                expense["category"],
                expense["date"],
                expense["note"]
            ])

    print("Expenses exported to expenses.csv")


parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    choices=["add", "list", "summary", "export"]
)

args = parser.parse_args()


if args.command == "add":
    add_expense()

elif args.command == "list":
    list_expenses()

elif args.command == "summary":
    summary()

elif args.command == "export":
    export_csv()
