from .main import (
    add_income, AddIncomeArgs,
    add_expense, AddExpenseArgs,
    view_expenses, ViewExpensesArgs,
    view_summary, ViewSummaryArgs,
    view_budget
)
from datetime import date

today = date.today().isoformat()
month = today[:7]

print("--- Add Income ---")
print(add_income(AddIncomeArgs(
    date=today,
    source="Freelance Work",
    amount=1200.0
)))

print("\n--- Add Expense ---")
print(add_expense(AddExpenseArgs(
    date=today,
    category="Groceries",
    amount=45.50,
    note="Weekly groceries"
)))

print("\n--- View Expenses ---")
print(view_expenses(ViewExpensesArgs(
    category="Groceries",
    date=month
)))

print("\n--- View Summary ---")
print(view_summary(ViewSummaryArgs(
    month=month
)))

print("\n--- View Budget ---")
print(view_budget())
