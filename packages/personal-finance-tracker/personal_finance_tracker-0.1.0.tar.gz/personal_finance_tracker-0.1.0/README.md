# Personal Finance Tracker (MCP Server)

A lightweight [MCP server](https://github.com/multiprompt/mcp) for tracking **personal** expenses, income, and budget summaries using SQLite.  
This server is designed for **individuals or households** — not for businesses or stock analysis.

---

## ✨ Features

- 📌 Record personal expenses and income
- 📊 View monthly summaries and budget overviews
- 📈 Analyze monthly spending trends
- ⚙️ Configurable database path (`DB_PATH`)

---

## 📦 Installation

Install from PyPI:

```bash
pip install personal-finance-tracker
```

---

## 🚀 Usage

You can run the server using:

```bash
uvx personal-finance-tracker
```

Or configure it in a client like [Cursor](https://cursor.so) or other MCP-compatible tools:

```jsonc
{
  "mcpServers": {
    "personal-finance-tracker": {
      "command": "uvx",
      "args": ["personal-finance-tracker"],
      "env": {
        "DB_PATH": "/absolute/path/to/your/finance.db"
      }
    }
  }
}
```

---

## 📁 Environment Variables

| Variable  | Description                              | Default         |
|-----------|------------------------------------------|-----------------|
| `DB_PATH` | Path to the SQLite database file         | `expenses.db`   |

The database file is created and initialized automatically if it doesn't exist.

---

## 🧠 Prompt Behavior

This MCP server is **specifically scoped for personal finance**. The underlying LLM is guided to:

✅ Use these tools when:
- The user asks about **daily expenses**, **personal income**, **budgeting**, **household savings**

🚫 Avoid using for:
- Business accounting
- Stock market analysis
- Corporate finance data

---

## 📂 Project Structure

```
personal-finance-tracker/
├── src/
│   └── personal_finance_tracker/
│       └── main.py
├── pyproject.toml
├── README.md
```

---

## 📝 License

ABRMS License
