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

## Day 9
- **Built:** Integrated AI to automatically categorize expenses into strict categories (Food, Transport, etc.) before saving to the database.
- **Learned:** How to use LLMs for structured data extraction rather than just conversational text. Also learned how to handle API errors (like rate limits) with fallback default values.
- **Struggled with:** The AI returning "Other" initially due to a bad model name and timeout errors. Fixed it by using the correct `gemini-3.8-flash` model and resetting the database.
- **Tomorrow:** Embeddings & Vector Databases (The foundation of RAG).

## Day 10
- **Built:** A local semantic search engine using `sentence-transformers` and `ChromaDB`.
- **Learned:** How embeddings turn text into mathematical vectors, and how vector databases find items based on *meaning* rather than exact keyword matches.
- **Struggled with:** A small `AttributeError` because `.tolist()` was called on a list that was already a Python list. Fixed by removing `.tolist()`.
- **Tomorrow:** Building a RAG (Retrieval-Augmented Generation) pipeline from scratch.

## Day 11
- **Built:** A complete RAG (Retrieval-Augmented Generation) pipeline from scratch. Reads a PDF, chunks it, embeds the chunks, stores them in ChromaDB, and uses Gemini to answer questions based *only* on the document.
- **Learned:** How to handle PDF extraction, the importance of chunking, and how to implement exponential backoff (retry logic) to handle API rate limits and server errors gracefully.
- **Struggled with:** API 503 errors and hallucinated model names. The retry logic and the `check_models.py` script solved it.
- **Tomorrow:** Building a beautiful chat UI for this RAG pipeline using Streamlit.

## Day 12
- **Built:** A ChatGPT-style web interface for the RAG pipeline using Streamlit.
- **Learned:** How to manage state across reruns using `st.session_state`, how to handle file uploads, and how to use `st.chat_input` and `st.chat_message`.
- **Struggled with:** A ChromaDB `where={}` error when trying to clear the database. Fixed it by deleting and recreating the collection entirely.
- **Tomorrow:** Building Project 2 (AI Resume-to-JD Analyzer).

## Day 13
- **Built:** Project 2 - An AI Resume Analyzer that compares a resume PDF against a Job Description.
- **Learned:** How to force an LLM to return strict JSON data using prompt engineering, how to parse that JSON in Python (`json.loads`), and how to dynamically render results with color-coded UI components in Streamlit.
- **Struggled with:** Handling empty PDFs (scanned images) by adding a text-extraction length check before calling the AI.
- **Tomorrow:** Deployment Day (Getting these apps off localhost!).

## Day 14
- **Built:** Deployed the FastAPI backend to Vercel and the Streamlit frontend to Streamlit Community Cloud.
- **Learned:** How to handle serverless read-only filesystems (using `/tmp` for SQLite), how to configure CORS for production, how to use `.vercelignore` and `requirements-vercel.txt` to keep deployment bundles small, and how to manage environment variables in the cloud.
- **Struggled with:** Vercel's 500 MB limit and SQLite's read-only error. Fixed them by splitting the requirements file and pointing the DB to `/tmp`.
- **Tomorrow:** Dockerizing the backend & updating the portfolio.

## Day 15
- **Built:** Created a `Dockerfile` to containerize the FastAPI backend.
- **Learned:** How to write a Dockerfile, build an image (`docker build`), and run a container (`docker run`). Also learned how to use Colima as a free Docker Desktop alternative on Mac.
- **Struggled with:** Fixing the `requirements-vercel.txt` path and ensuring Colima was running properly.
- **Tomorrow:** Building the Portfolio Website to showcase these live links.

## Day 16
- **Built:** A live, professional portfolio website using Streamlit and custom CSS.
- **Learned:** How to manage multiple deployments from a single GitHub repository, how to style Streamlit apps with HTML/CSS, and how to handle conflicting dependency requirements (google-genai vs google-generativeai).
- **Struggled with:** Streamlit Cloud's caching of old requirements. Fixed it by forcing redeployments and updating the requirements file.
- **Tomorrow:** Cleaning up the GitHub repository and writing professional READMEs for the projects.

## Day 16 & 17: Cloud Deployment & Professional Polish

### The Vercel Saga
- **Built:** Deployed the FastAPI backend to Vercel.
- **Learned:** Discovered that Vercel's serverless platform has a 500MB bundle limit and a read-only filesystem. Learned how to use `/tmp` for SQLite and `.vercelignore` to shrink bundles.
- **Struggled with:** A persistent "Phantom 404" routing error where Vercel would only serve the root endpoint, ignoring all `/expenses` routes.

### The Railway Migration
- **Built:** Migrated the FastAPI backend to Railway (a persistent server host). Successfully connected the Streamlit frontend to the live Railway URL.
- **Learned:** How to debug Docker build checksums, how to fix `uvicorn: command not found`, and how to properly set environment variables (`GEMINI_API_KEY`) in a cloud dashboard.
- **Struggled with:** Correcting the `ModuleNotFoundError: No module named 'api'` by properly structuring the repository.

### The Makeover
- **Built:** Restructured the repository into a monorepo (`api/` for backend, `streamlit_apps/` for frontend) to separate heavy AI dependencies from the lightweight backend. Wrote a professional `README.md` with live links and architecture details.
- **Tomorrow:** LeetCode, System Design, and starting the job application blitz.