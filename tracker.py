# ==============================
# Expense Class
# ==============================

class Expense:
    def __init__(self, expense_id, date, category, description, amount):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.description = description
        self.amount = float(amount)

    def to_list(self):
        """Convert object to list (for CSV writing)."""
        return [self.expense_id, self.date, self.category, self.description, str(self.amount)]

class ExpenseManager:
    FILE_NAME = "expenses.csv"

    def __init__(self):
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Date", "Category", "Description", "Amount"])  # Header

    def _read_expenses(self):
        expenses = []
        with open(self.FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(Expense(row["ID"], row["Date"], row["Category"], row["Description"], row["Amount"]))
        return expenses

    def _write_expenses(self, expenses):
        with open(self.FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Description", "Amount"])
            for exp in expenses:
                writer.writerow(exp.to_list())

    def add_expense(self, category, description, amount):
        expenses = self._read_expenses()
        expense_id = str(len(expenses) + 1)
        date = datetime.now().strftime("%Y-%m-%d")
        new_exp = Expense(expense_id, date, category, description, amount)

        with open(self.FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_exp.to_list())

        print(f" Expense added: {description} - ${amount}")

    def view_expenses(self):
        expenses = self._read_expenses()
        if not expenses:
            print(" No expenses found.")
            return
        print("\n--- All Expenses ---")
        for exp in expenses:
            print(f"[{exp.expense_id}] {exp.date} | {exp.category} | {exp.description} | ${exp.amount:.2f}")

    def update_expense(self, expense_id, category=None, description=None, amount=None):
        expenses = self._read_expenses()
        found = False
        for exp in expenses:
            if exp.expense_id == expense_id:
                if category: exp.category = category
                if description: exp.description = description
                if amount: exp.amount = float(amount)
                found = True
                break
        if found:
            self._write_expenses(expenses)
            print(" Expense updated successfully.")
        else:
            print(" Expense ID not found.")

    def delete_expense(self, expense_id):
        expenses = self._read_expenses()
        updated_expenses = [exp for exp in expenses if exp.expense_id != expense_id]

        if len(updated_expenses) == len(expenses):
            print(" Expense ID not found.")
            return

        # Reassign IDs
        for idx, exp in enumerate(updated_expenses, 1):
            exp.expense_id = str(idx)

        self._write_expenses(updated_expenses)
        print(" Expense deleted successfully.")

    def search_by_category(self, category):
        expenses = self._read_expenses()
        filtered = [exp for exp in expenses if exp.category.lower() == category.lower()]
        if filtered:
            print(f"\n--- Expenses in Category: {category} ---")
            for exp in filtered:
                print(f"[{exp.expense_id}] {exp.date} | {exp.description} | ${exp.amount:.2f}")
        else:
            print("⚠️ No expenses found in this category.")

    def show_summary(self):
        expenses = self._read_expenses()
        if not expenses:
            print("⚠️ No expenses to summarize.")
            return

        total = sum(exp.amount for exp in expenses)
        print(f"\n💰 Total Spent: ${total:.2f}")

        category_summary = {}
        for exp in expenses:
            category_summary[exp.category] = category_summary.get(exp.category, 0) + exp.amount

        print("\n--- Category Breakdown ---")
        for cat, amt in category_summary.items():
            print(f"{cat}: ${amt:.2f}")