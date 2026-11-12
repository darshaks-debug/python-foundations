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

---

### Day 17: Cloud Deployment, Monorepo Infrastructure & Professional Polish

- **Built:** Successfully deployed the FastAPI backend to the cloud (migrated from Vercel to Railway). Restructured the repository into a monorepo (`api/` for the backend, `streamlit_apps/` for the frontend) to separate heavy AI dependencies from the lightweight backend. Wrote a professional `README.md` with live links and architecture details.
- **Learned:** Discovered Vercel's serverless limitations (500MB bundle limit, read-only filesystem). Learned how to configure Railway's environment variables, start commands, and root directories. Learned how to force a dark theme in Streamlit using `config.toml` and resolved a Git merge conflict.
- **Struggled with:** Vercel's "Phantom 404" routing errors, Railway's Docker build checksums, `uvicorn: command not found`, and fixing the `ModuleNotFoundError` by properly setting the root directory.
- **Tomorrow:** Upgrading the database from SQLite to PostgreSQL.

## Day 18
- **Built:** Migrated the database from SQLite to a persistent PostgreSQL database hosted on Railway. 
- **Learned:** How to provision a cloud database, how to use environment variables (`DATABASE_URL`) to connect the backend to the database securely, and how to handle the `postgres://` vs `postgresql://` URL prefix issue.
- **Struggled with:** Ensuring the `psycopg2-binary` driver was installed correctly. Proved persistence by restarting the server and verifying data remained intact.
- **Tomorrow:** Adding User Authentication (JWT) to make the app secure.

## Day 19
- **Built:** Implemented JWT (JSON Web Token) authentication. Added User Registration and Login endpoints. Secured all expense endpoints so users can only see, add, and delete their own data. Deployed the secure backend to Railway.
- **Learned:** How to hash passwords securely using Argon2 (`pwdlib`), how to generate and verify JWTs, and how to use FastAPI's `Depends` to protect specific routes. 
- **Struggled with:** The `passlib` / `bcrypt` compatibility error (fixed by switching to `pwdlib`) and resetting the Railway database to accommodate the new `owner_id` schema.
- **Tomorrow:** Updating the Streamlit frontend to handle Login/Signup and pass the JWT token to the backend.

## Day 20
- **Built:** Login/Register UI in Streamlit with JWT sent in request headers; moved SECRET_KEY out of source code into environment variables on Railway and locally.
- **Learned:** Why secrets never belong in a repo, how `load_dotenv()` ordering matters, and how fail-fast startup checks surface config problems in deploy logs.
- **Struggled with:** The app refusing to start locally until SECRET_KEY was in `.env`, which showed the check was working.
- **Tomorrow:** Alembic database migrations.

## Day 21
- **Built:** Integrated Alembic for database migrations. Removed `create_all()` so Alembic owns the schema. Generated an initial migration capturing the `users` and `expenses` tables, applied it locally and to Railway via the start command.
- **Learned:** Why teams never delete production databases to change schema. How Alembic autogenerates migrations by diffing models against the DB. How to read the generated migration file before applying it.
- **Struggled with:** Configuring `env.py` to import models correctly from `expense_api.py`, ensuring `alembic.ini` lives inside `api/`, and fixing the `ModuleNotFoundError: No module named 'psycopg'` by adding `psycopg[binary]` to the requirements.
- **Tomorrow:** Pytest — writing tests for the auth and expense endpoints.

## Day 22
- **Built:** Wrote automated tests for the FastAPI backend using Pytest. Created fixtures to override the database session with an in-memory SQLite DB for fast, isolated testing. Wrote tests for registration, login, unauthorized access, and cross-user data isolation.
- **Learned:** How to use `TestClient` from FastAPI, how to mock dependencies (`app.dependency_overrides`), and how to structure a testing suite.
- **Struggled with:** Fixing the `ModuleNotFoundError` by using `python3 -m pytest` and adjusting the `sys.path` in `conftest.py`. Also fixed the `datetime.utcnow()` deprecation warning.
- **Tomorrow:** Setting up GitHub Actions for CI/CD.

## Day 23
- **Built:** Set up a CI/CD pipeline using GitHub Actions. The workflow automatically runs the Pytest suite on every push to the main branch.
- **Learned:** How to write a YAML workflow file, how to set up GitHub Actions to use Python 3.12, and how to inject dummy environment variables into a CI environment.
- **Struggled with:** Ensuring the `.github` folder was at the repository root, not inside the `api/` folder, so GitHub could detect it.
- **Tomorrow:** Researching 20 job descriptions and polishing the resume.

## Day 24
- **Built:** Translated technical projects into impact-driven resume bullet points. Updated LinkedIn profile to reflect Python Backend and AI Engineering skills.
- **Learned:** Analyzed 20 real job descriptions to map market demand for specific skills (FastAPI, Postgres, Docker). Practiced SQL Joins.
- **Struggled with:** Trimming down the resume to focus on metrics and outcomes rather than just listing tools and trials.
- **Tomorrow:** Making the RAG app production-ready with per-user document isolation.