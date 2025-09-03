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
