import json

FILE_NAME = "expenses.json"

# Load data from file
def load_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            data = file.read()
            if data.strip() == "":
                return []
            return json.loads(data)
    except FileNotFoundError:
        return []

# Save data to file
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)

# Load existing data
expenses = load_expenses()


# Add expense
def add_expense():
    amount = int(input("Enter amount: "))
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD): ")

    expense = {
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("✅ Expense added & saved!\n")


# View expenses
def view_expenses():
    if len(expenses) == 0:
        print("❌ No expenses found\n")
    else:
        print("\n------ All Expenses ------")
        for i, e in enumerate(expenses, start=1):
            print(f"{i}. Amount: {e['amount']}, Category: {e['category']}, Date: {e['date']}")
        print("--------------------------\n")


# Delete expense
def delete_expense():
    if len(expenses) == 0:
        print("❌ No expenses to delete\n")
        return

    view_expenses()

    try:
        index = int(input("Enter expense number to delete: ")) - 1

        if 0 <= index < len(expenses):
            expenses.pop(index)
            save_expenses(expenses)
            print("🗑️ Expense deleted successfully!\n")
        else:
            print("❌ Invalid number\n")

    except:
        print("❌ Please enter a valid number\n")


# Update expense
def update_expense():
    if len(expenses) == 0:
        print("❌ No expenses to update\n")
        return

    view_expenses()

    try:
        index = int(input("Enter expense number to update: ")) - 1

        if 0 <= index < len(expenses):
            print("Leave blank to keep old value")

            new_amount = input("Enter new amount: ")
            new_category = input("Enter new category: ")
            new_date = input("Enter new date (YYYY-MM-DD): ")

            if new_amount:
                expenses[index]["amount"] = int(new_amount)
            if new_category:
                expenses[index]["category"] = new_category
            if new_date:
                expenses[index]["date"] = new_date

            save_expenses(expenses)

            print("✏️ Expense updated successfully!\n")
        else:
            print("❌ Invalid number\n")

    except:
        print("❌ Please enter a valid number\n")


# Total expense
def total_expense():
    total = sum(e["amount"] for e in expenses)
    print(f"\n💰 Total Expense: {total}\n")


# Search by category
def search_by_category():
    category = input("Enter category to search: ")

    found = False

    for e in expenses:
        if e["category"].lower() == category.lower():
            print(f"Amount: {e['amount']}, Date: {e['date']}")
            found = True

    if not found:
        print("❌ No matching expenses found\n")


# Main menu loop
while True:
    print("========== EXPENSE TRACKER ==========")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Update Expense")
    print("5. Total Expense")
    print("6. Search by Category")
    print("7. Exit")
    print("====================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        delete_expense()

    elif choice == "4":
        update_expense()

    elif choice == "5":
        total_expense()

    elif choice == "6":
        search_by_category()

    elif choice == "7":
        print("Exiting... Data saved!")
        break

    else:
        print("❌ Invalid choice. Try again.\n")