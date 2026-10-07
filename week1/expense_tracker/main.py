import argparse
import csv
from datetime import datetime

from models import create_expense
from storage import add_expense, load_expenses, monthly_summary


def add_expense_command():
    try:
        amount = float(input("Amount = "))

        if amount < 0:
            print("Invalid amount: amount cannot be negative.")
            return

        category = input("Category = ")
        date = input("Date (YYYY-MM-DD) = ")

        datetime.strptime(date, "%Y-%m-%d")

        note = input("Note = ")

        expense = create_expense(
            amount,
            category,
            date,
            note,
        )

        add_expense(expense)

        print("Expense Added")

    except ValueError:
        print(
            "Invalid input. Please enter a valid amount "
            "and date (YYYY-MM-DD)."
        )


def list_expenses():
    expenses = load_expenses()

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
    results = monthly_summary()

    if not results:
        print("No expenses found.")
        return

    for month, total in results:
        print(f"{month.strftime('%Y-%m')}: {total}")


def export_csv():
    expenses = load_expenses()

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "amount",
                "category",
                "date",
                "note",
            ]
        )

        for expense in expenses:
            writer.writerow(
                [
                    expense["amount"],
                    expense["category"],
                    expense["date"],
                    expense["note"],
                ]
            )

    print("Expenses exported to expenses.csv")


parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    choices=["add", "list", "summary", "export"],
)

args = parser.parse_args()


if args.command == "add":
    add_expense_command()

elif args.command == "list":
    list_expenses()

elif args.command == "summary":
    summary()

elif args.command == "export":
    export_csv()