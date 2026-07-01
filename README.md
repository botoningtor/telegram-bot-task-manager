# 📝 Telegram Task Manager Bot

An asynchronous Telegram bot designed for managing personal tasks and notes. The project is built using the `aiogram 3.x` framework with a clean, layered architecture (Handlers, Keyboards, Services, Models) and asynchronous database interaction powered by `SQLAlchemy 2.0`.

---

## 🛠 Tech Stack

*   **Framework:** [aiogram 3.x](https://github.com) (Asynchronous Telegram Bot API)
*   **State Management:** FSM (Finite State Machine) for handling multi-step dialogues
*   **Database:** SQLite (via `aiosqlite` driver)
*   **ORM:** [SQLAlchemy 2.0](https://github.com) (Async sessions & Declarative Mapping)
*   **Configuration:** Pydantic Settings (Environment variables validation via `.env`)

---

## 📂 Project Structure

```text
task_manager/
│
├── handlers/               # Event handlers for commands, text messages, and callbacks
│   ├── start.py            # /start command handler & user registration
│   └── tasks.py            # FSM scenarios, task listing, status toggling, and deletion
│
├── keyboards/              # Keyboard generation modules
│   └── menu.py             # Main Reply-menu and interactive Inline-keyboards
│
├── services/               # Business logic and database operations
│   └── task_service.py     # CRUD operations for users and tasks
│
├── bot.py                  # Main entry point for bot initialization and execution
├── config.py               # Application configuration using Pydantic
├── database.py             # Asynchronous database engine and session setup
├── models.py               # Declarative ORM models for database tables
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## 🗄 Database Schema (SQLite)

The project utilizes a relational data structure with cascade deletion constraints:

### `users` Table

| Field | Data Type | Description |
| :--- | :--- | :--- |
| **id** `(PK)` | `INTEGER` | Unique internal user identifier |
| **telegram_id** | `BIGINT` | Unique Telegram ID of the user (indexed) |
| **username** | `VARCHAR` | Telegram username (nullable) |

### `tasks` Table

| Field | Data Type | Description |
| :--- | :--- | :--- |
| **id** `(PK)` | `INTEGER` | Unique internal task identifier |
| **user_id** `(FK)` | `INTEGER` | Reference to `users.id` (ON DELETE CASCADE) |
| **title** | `VARCHAR` | The text/title of the task |
| **completed** | `BOOLEAN` | Task execution status (`False` by default) |

---

## 🚀 Local Deployment Guide

### 1. Clone the Repository
```bash
git clone https://github.com/botoningtor/telegram-bot-task-manager
cd YOUR_REPOSITORY_NAME
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Telegram Bot Token obtained from [@BotFather](https://t.me):
```env
   BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
   DB_URL=sqlite+aiosqlite:///tasks.db
```

### 5. Run the Bot
The SQLite database and all required tables will be generated automatically upon the first application startup.
```bash
   python bot.py
```
