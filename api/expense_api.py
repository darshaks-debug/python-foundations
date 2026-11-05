from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List, Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load the API Key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- 1. DATABASE SETUP ---
# Get the DATABASE_URL from Railway. If it doesn't exist (local testing), fallback to SQLite.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/expenses.db")

# Railway gives us a URL starting with "postgres://", but SQLAlchemy needs "postgresql://"
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite requires a special argument that PostgreSQL does not.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. THE DATABASE MODEL ---
class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    category = Column(String, default="Uncategorized")

Base.metadata.create_all(bind=engine)

# --- 3. THE PYDANTIC MODEL ---
class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    description: str
    category: Optional[str] = "Uncategorized"

    class Config:
        orm_mode = True

# --- 4. DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. FASTAPI APP ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows Streamlit Cloud to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/expenses", response_model=List[Expense])
def list_expenses(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    return expenses

@app.post("/expenses")
def add_expense(new_expense: Expense, db: Session = Depends(get_db)):
    prompt = f"""
    Categorize this expense into exactly ONE of these categories: 
    [Food, Transport, Entertainment, Bills, Shopping, Other].
    Only reply with the category name. Do not add punctuation or extra words.
    
    Expense: {new_expense.description}
    """
    
    assigned_category = "Other"
    
    try:
        # FIXED MODEL NAME HERE
        model = genai.GenerativeModel('gemini-3.5-flash') 
        response = model.generate_content(prompt)
        if response.text:
            assigned_category = response.text.strip().capitalize() 
    except Exception as e:
        print(f"AI Error: {e}")

    db_expense = ExpenseDB(
        amount=new_expense.amount, 
        description=new_expense.description,
        category=assigned_category
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return {"message": "Expense added", "expense": db_expense}

@app.get("/expenses/total")
def get_total(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    total = sum(exp.amount for exp in expenses)
    return {"total_expenses": total}

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": f"Expense {expense_id} deleted successfully."} # FIXED PLACEMENT

@app.get("/expenses/analyze")
def analyze_expenses(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    if not expenses:
        return {"analysis": "You have no expenses to analyze."}
        
    expense_text = "\n".join([f"- {exp.description}: ₹{exp.amount}" for exp in expenses])
    prompt = f"""
    You are a helpful financial advisor. Here is a list of my recent expenses:
    {expense_text}
    Please provide a short, 3-sentence analysis of my spending. 
    Give me one specific tip on how to save money based on these expenses.
    """
    
    try:
        # FIXED MODEL NAME HERE
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(prompt)
        return {"analysis": response.text}
    except Exception as e:
        print(f"BACKEND ERROR: {e}")
        return {"error": str(e)}
@app.get("/")
def read_root():
    return {"message": "Expense Tracker API is live on Vercel!"}