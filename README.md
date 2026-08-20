# 📚 Book & Expenses Tracker Backend

A modular, production-ready FastAPI backend application for managing books and tracking daily expenses. Built with modern Python tools and SQLAlchemy 2.0 type hinting.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) / [SQLModel](https://sqlmodel.tiangolo.com/)
* **Data Validation & Settings:** [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings`
* **Database:** SQLite
* **Environment Management:** `python-dotenv`

---

## 📁 Project Structure

```text
Book_and_expenses_tracker_backend/
│
├── router/                  # API route handlers
│   ├── __init__.py
│   ├── books.py             # CRUD endpoints for books
│   └── expenses.py          # CRUD endpoints for expenses
│
├── settings/                # Application configurations
│   ├── __init__.py
│   └── general_settings.py  # Pydantic BaseSettings class
│
├── database.py              # Database connection, engine, and ORM models
├── main.py                  # Application entry point (Lifespan & App Setup)
├── .env                     # Local environment variables (git-ignored)
├── .env.example             # Template for environment variables
├── .gitignore               # Git ignored files and directories
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/fakhrianabusi/Book_and_expenses_tracker_backend.git
cd Book_and_expenses_tracker_backend
```

### 2. Create & Activate a Virtual Environment

**On Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**On Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (.env)

Create a `.env` file in the root directory and add the following settings:

```env
APP_TITLE=FastAPI Book and Expenses tracker
VERSION=0.1.0
DATABASE_URL=sqlite:///./store.db
ECHO=True
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The server will start running locally at: **http://127.0.0.1:8000**

---

## 📖 Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can explore and test the endpoints via:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 📚 Books API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| POST | `/books/` | Create a new book entry | 201 Created |
| GET | `/books/` | Retrieve all books | 200 OK |
| GET | `/books/{id}` | Get details of a specific book | 200 OK |
| PUT | `/books/{id}` | Update an existing book entry | 200 OK |
| DELETE | `/books/{id}` | Delete a book record | 200 OK |

---

## 💰 Expenses API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| POST | `/expenses/` | Record a new expense | 201 Created |
| GET | `/expenses/` | List expenses (supports filtering & pagination) | 200 OK |
| GET | `/expenses/{id}` | Get details of a specific expense | 200 OK |
| PATCH | `/expenses/{id}` | Partially update an expense record | 200 OK |
| DELETE | `/expenses/{id}` | Delete an expense record | 200 OK |

---

## 🔧 Configuration

The application uses `pydantic-settings` for environment variable management. Configuration is loaded from the `.env` file and can be customized based on your deployment needs.

### Available Settings

- `APP_TITLE`: Application name displayed in API documentation
- `VERSION`: API version number
- `DATABASE_URL`: Database connection string
- `ECHO`: Enable/disable SQL query logging (True/False)

---

## 🗄️ Database

The application uses **SQLite** as the database, which stores data in a local file (`store.db` by default). The database schema is automatically created using SQLAlchemy 2.0 ORM models defined in `database.py`.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Fakhri Anabusi**

- GitHub: [@fakhrianabusi](https://github.com/fakhrianabusi)

---

## 📞 Support

If you have any questions or need help with setup, please open an issue on GitHub.