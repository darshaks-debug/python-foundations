# python-foundations

# Progress Log

## Day 1
- **Built:** A looping calculator with input validation.
- **Learned:** `try/except` blocks, `while True` loops, how to fix IndentationError, and how to push to GitHub.
- **Struggled with:** Indenting the `except` blocks correctly.
- **Tomorrow:** Conditionals, loops, functions.

## Day 2
- **Built:** 8 practice problems (functions, loops), Grade Calculator, and Number Guessing Game.
- **Learned:** How to write `def` functions, the difference between `print` and `return`, and how to use nested `while` loops.
- **Struggled with:** Remembering to add the `except ValueError` block inside the `try` statement.
- **Tomorrow:** Data structures (Lists, Dicts, Sets) and the Expense Tracker CLI.

## Day 3
- **Built:** 10 practice problems (Lists, Sets, Dicts) and a JSON-backed Expense Tracker CLI.
- **Learned:** How to use dictionaries effectively, how to do `json.load()` and `json.dump()`, and how to use `continue` to skip bad inputs.
- **Struggled with:** Indentation in VS Code when pasting code. (Lesson learned: type it out or use Format Document!).
- **Tomorrow:** FastAPI — building my first web API!

## Day 4
- **Built:** A fully functional REST API using FastAPI. Includes GET, POST, and dynamic total calculation.
- **Learned:** How to use Uvicorn, how Pydantic automatically validates data, how path/query parameters work, and how to test APIs via Swagger UI (`/docs`).
- **Struggled with:** The 500 Internal Server Error caused by old JSON data. Learned that deleting the corrupted file and using `.dict()` fixed it.
- **Tomorrow:** Connecting a frontend to the backend (Streamlit) or diving deeper into FastAPI.

## Day 5
- **Built:** A full-stack Expense Tracker with a Streamlit frontend connected to a FastAPI backend.
- **Learned:** How to send HTTP requests using the `requests` library, how to build interactive forms in Streamlit, and how to display data tables and charts.
- **Struggled with:** Forgetting parentheses on `st.divider()`.
- **Tomorrow:** Connecting a real database (SQLite) or moving on to AI/LLM integration.

## Day 6
- **Built:** Replaced the JSON file with a SQLite database using SQLAlchemy.
- **Learned:** How ORMs (Object-Relational Mappers) work, how to define database tables using Python classes, and how to manage database sessions in FastAPI using `Depends`.
- **Struggled with:** Accidentally pasting the backend code into `frontend.py` and deleting the old JSON file.
- **Tomorrow:** Completing CRUD operations (adding a Delete button) and maybe adding some AI magic.

## Day 7
- **Built:** Added full Delete functionality (CRUD) to the API and the Streamlit UI.
- **Learned:** How to use `db.delete()` in SQLAlchemy, how to pass path parameters (`/expenses/{id}`), how to handle HTTP 404 exceptions, and how to build dynamic UI rows with buttons in Streamlit.
- **Struggled with:** Nested quotes in f-strings causing a SyntaxError, and fixing the `KeyError` by updating the Pydantic model to include `id`.
- **Tomorrow:** We are officially one week in! Time to bring in the AI.

## Day 8
- **Built:** Integrated Google Gemini API to analyze expenses and provide financial advice.
- **Learned:** How to use `python-dotenv` to secure API keys, how to format prompts, and how to handle rate limits (429 errors) and model availability (404 errors).
- **Struggled with:** Finding the correct model name (`gemini-2.5-flash`) and dealing with the free-tier rate limits.
- **Tomorrow:** Advanced Prompt Engineering (getting the AI to return structured JSON data).