"""A simple command-line expense tracker. Data is saved in expenses.json."""
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.json")
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]


def load_expenses():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("Could not read expenses.json. Starting with an empty list.")
        return []


def save_expenses(expenses):
    DATA_FILE.write_text(json.dumps(expenses, indent=4), encoding="utf-8")


def add_expense(expenses):
    description = input("What was the expense for? ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Amount (₹): ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid amount greater than zero.")
        return

    print("\nCategories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")
    choice = input("Choose a category (1-6): ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(CATEGORIES):
        print("Invalid category.")
        return

    expenses.append({
        "description": description,
        "amount": round(amount, 2),
        "category": CATEGORIES[int(choice) - 1],
        "date": date.today().isoformat(),
    })
    save_expenses(expenses)
    print("Expense saved successfully!")


def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\n--- All Expenses ---")
    for number, item in enumerate(expenses, start=1):
        print(
            f"{number}. {item['date']} | {item['category']} | "
            f"{item['description']} | ₹{item['amount']:.2f}"
        )


def show_summary(expenses):
    if not expenses:
        print("\nNo expenses to summarize.")
        return
    total = sum(item["amount"] for item in expenses)
    by_category = {}
    for item in expenses:
        category = item["category"]
        by_category[category] = by_category.get(category, 0) + item["amount"]

    print("\n--- Spending Summary ---")
    print(f"Total expenses: ₹{total:.2f}")
    print(f"Number of expenses: {len(expenses)}")
    print("\nBy category:")
    for category, amount in sorted(by_category.items()):
        print(f"- {category}: ₹{amount:.2f}")


def main():
    expenses = load_expenses()
    while True:
        print("\n====== Expense Tracker ======")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. View spending summary")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
            expenses = load_expenses()
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            print("Thanks for using Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
