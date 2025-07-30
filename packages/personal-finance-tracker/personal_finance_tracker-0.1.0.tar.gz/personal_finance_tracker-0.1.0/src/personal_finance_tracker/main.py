from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from collections import defaultdict
import sqlite3
import os

# ---------------------- Configuration ----------------------
DB_PATH = os.environ.get("DB_PATH", "expenses.db")

# ---------------------- Database Initialization ----------------------
def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    note TEXT
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    amount REAL NOT NULL
                )
            """)
            conn.commit()

# Initialize DB only if needed
init_db()

# ---------------------- MCP Setup ----------------------
mcp = FastMCP(
    name="PersonalFinanceTracker",
    description="Track personal finances — record expenses and income, and view budget summaries. Use only for individual or household-level financial tracking.",
    dependencies=["sqlite3"],
    instructions=(
        "Use these tools when a user refers to their *personal* budget, income, or spending habits. "
        "This is **not** intended for business finances, stock analysis, corporate accounting, or financial markets. "
        "If the user's question is about personal savings, grocery expenses, rent, or income from a job, then use this MCP."
    )
)

# ---------------------- Argument Schemas ----------------------
class AddExpenseArgs(BaseModel):
    date: str = Field(..., description="Date of the expense in YYYY-MM-DD format")
    category: str = Field(..., description="Category of the expense")
    amount: float = Field(..., description="Amount spent")
    note: Optional[str] = Field("", description="Optional description or note")

class ViewExpensesArgs(BaseModel):
    category: Optional[str] = Field("", description="(Optional) Filter by category")
    date: Optional[str] = Field("", description="(Optional) Filter by YYYY-MM or YYYY-MM-DD")

class ViewSummaryArgs(BaseModel):
    month: str = Field(..., description="Target month for summary in YYYY-MM format")

class AddIncomeArgs(BaseModel):
    date: str = Field(..., description="Date income was received in YYYY-MM-DD format")
    source: str = Field(..., description="Source of the income")
    amount: float = Field(..., description="Amount of income")

# ---------------------- Helpers ----------------------
def get_connection():
    return sqlite3.connect(DB_PATH)

# ---------------------- MCP Tools ----------------------
@mcp.tool(annotations={"title": "Add Personal Expense", "description": "Record a new personal expense in the database."})
def add_expense(args: AddExpenseArgs) -> str:
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        return "❌ Invalid date format. Use YYYY-MM-DD."

    with get_connection() as conn:
        conn.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                     (args.date, args.category, args.amount, args.note))
    return "✅ Expense added."

@mcp.tool(annotations={"title": "View Personal Expenses", "description": "Retrieve personal expense records with optional filters by category or date."})
def view_expenses(args: ViewExpensesArgs) -> str:
    query = "SELECT date, category, amount, note FROM expenses WHERE 1=1"
    params = []
    if args.category:
        query += " AND category = ?"
        params.append(args.category)
    if args.date:
        query += " AND date LIKE ?"
        params.append(args.date + "%")

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    if not rows:
        return "⚠️ No expenses found."

    return "\n".join(["--- Filtered Personal Expenses ---"] + [f"{row[0]} | {row[1]} | ${row[2]:.2f} | {row[3]}" for row in rows])

@mcp.tool(annotations={"title": "View Monthly Summary", "description": "Summarize total personal expenses by category for a given month."})
def view_summary(args: ViewSummaryArgs) -> str:
    with get_connection() as conn:
        rows = conn.execute("SELECT category, amount FROM expenses WHERE date LIKE ?", (args.month + '%',)).fetchall()

    if not rows:
        return f"⚠️ No expenses found for {args.month}."

    summary = defaultdict(float)
    total = 0.0
    for cat, amt in rows:
        summary[cat] += amt
        total += amt

    lines = [f"--- Summary for {args.month} ---"] + [f"{cat}: ${amt:.2f}" for cat, amt in summary.items()]
    lines.append(f"Total: ${total:.2f}")
    return "\n".join(lines)

@mcp.tool(annotations={"title": "Analyze Personal Spending", "description": "Analyze monthly personal spending trends."})
def analyze_expenses() -> str:
    with get_connection() as conn:
        rows = conn.execute("SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses GROUP BY month").fetchall()

    if not rows:
        return "⚠️ No data available."

    return "\n".join(["--- Monthly Spending ---"] + [f"{month}: ${total:.2f}" for month, total in rows])

@mcp.tool(annotations={"title": "Add Personal Income", "description": "Add a record of personal income."})
def add_income(args: AddIncomeArgs) -> str:
    with get_connection() as conn:
        conn.execute("INSERT INTO income (date, source, amount) VALUES (?, ?, ?)",
                     (args.date, args.source, args.amount))
    return "✅ Income recorded."

@mcp.tool(annotations={"title": "View Budget Overview", "description": "View total personal income, expenses, and net balance."})
def view_budget() -> str:
    with get_connection() as conn:
        income_total = conn.execute("SELECT SUM(amount) FROM income").fetchone()[0] or 0.0
        expense_total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0.0

    balance = income_total - expense_total
    return f"--- Personal Budget Overview ---\nIncome: ${income_total:.2f}\nExpenses: ${expense_total:.2f}\nBalance: ${balance:.2f}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()