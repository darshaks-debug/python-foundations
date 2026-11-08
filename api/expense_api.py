# --- IMPORTS ---
import os
from dotenv import load_dotenv

# load_dotenv() MUST run before any os.getenv() call.
# Do not let a formatter move this below the imports.
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List, Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pwdlib import PasswordHash
from google import genai  # New SDK


# --- SECURITY CONFIG ---
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- GEMINI CONFIG (New SDK) ---
# The new SDK uses a centralized Client object.
# It automatically picks up the GEMINI_API_KEY environment variable.
gemini_client = genai.Client()


# --- 1. DATABASE SETUP ---
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/expenses.db")

# Railway gives "postgres://"; SQLAlchemy needs "postgresql://"
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs check_same_thread; Postgres does not
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- 2. DATABASE MODELS ---
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    category = Column(String, default="Uncategorized")
    owner_id = Column(Integer, index=True)


# ❌ Base.metadata.create_all() is REMOVED. Alembic now owns the schema.


# --- 3. PYDANTIC MODELS ---
class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    description: str
    category: Optional[str] = "Uncategorized"

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str


# --- 4. HELPER FUNCTIONS & DEPENDENCIES ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# --- 5. FASTAPI APP ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 6. AUTH ENDPOINTS ---
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = UserDB(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- 7. PROTECTED EXPENSE ENDPOINTS ---
@app.get("/expenses", response_model=List[Expense])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expenses = db.query(ExpenseDB).filter(ExpenseDB.owner_id == current_user.id).all()
    return expenses


@app.post("/expenses")
def add_expense(
    new_expense: Expense,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    prompt = f"""
    Categorize this expense into exactly ONE of these categories: 
    [Food, Transport, Entertainment, Bills, Shopping, Other].
    Only reply with the category name. Do not add punctuation or extra words.
    
    Expense: {new_expense.description}
    """

    assigned_category = "Other"

    try:
        # New SDK syntax: client.models.generate_content
        response = gemini_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        if response.text:
            assigned_category = response.text.strip().capitalize()
    except Exception as e:
        print(f"AI Error: {e}")

    db_expense = ExpenseDB(
        amount=new_expense.amount,
        description=new_expense.description,
        category=assigned_category,
        owner_id=current_user.id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return {"message": "Expense added", "expense": db_expense}


@app.get("/expenses/total")
def get_total(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expenses = db.query(ExpenseDB).filter(ExpenseDB.owner_id == current_user.id).all()
    total = sum(exp.amount for exp in expenses)
    return {"total_expenses": total}


@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expense = (
        db.query(ExpenseDB)
        .filter(ExpenseDB.id == expense_id, ExpenseDB.owner_id == current_user.id)
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found or you don't have permission",
        )

    db.delete(expense)
    db.commit()
    return {"message": f"Expense {expense_id} deleted successfully."}


@app.get("/expenses/analyze")
def analyze_expenses(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expenses = db.query(ExpenseDB).filter(ExpenseDB.owner_id == current_user.id).all()

    if not expenses:
        return {"analysis": "You have no expenses to analyze."}

    expense_text = "\n".join(
        [f"- {exp.description}: ₹{exp.amount}" for exp in expenses]
    )
    prompt = f"""
    You are a helpful financial advisor. Here is a list of my recent expenses:
    {expense_text}
    Please provide a short, 3-sentence analysis of my spending. 
    Give me one specific tip on how to save money based on these expenses.
    """

    try:
        # New SDK syntax
        response = gemini_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        return {"analysis": response.text}
    except Exception as e:
        print(f"AI ERROR: {e}")
        assigned_category = f"Error: {str(e)[:20]}" #Shows the first 20 characters of the error in the category field


@app.get("/")
def read_root():
    return {"message": "Expense Tracker API is live. Schema managed by Alembic."}