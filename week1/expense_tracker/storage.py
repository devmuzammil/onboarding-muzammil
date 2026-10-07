import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def add_expense(expense):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (amount, category, date, note)
        VALUES (%s, %s, %s, %s)
        """,
        (
            expense["amount"],
            expense["category"],
            expense["date"],
            expense["note"],
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()


def load_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT amount, category, date, note
        FROM expenses
        ORDER BY date
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    expenses = []

    for row in rows:
        expenses.append(
            {
                "amount": float(row[0]),
                "category": row[1],
                "date": str(row[2]),
                "note": row[3],
            }
        )

    return expenses


def monthly_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(amount) AS total
        FROM expenses
        GROUP BY DATE_TRUNC('month', date)
        ORDER BY month
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows