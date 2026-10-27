from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List, Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv

#Load the API Key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- 1. DATABASE SETUP ---
# This creates a file called "expenses.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# This is the "session" - it's how we talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. THE DATABASE MODEL (SQLAlchemy) ---
# This defines the table structure in the database
class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# --- 3. THE PYDANTIC MODEL (For API validation) ---
class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    description: str

    class Config:
        orm_mode = True # Allows Pydantic to read SQLAlchemy models

# --- 4. DEPENDENCY (Yields a database session) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. FASTAPI APP ---
app = FastAPI()

@app.get("/expenses", response_model=List[Expense])
def list_expenses(db: Session = Depends(get_db)):
    # Query all rows from the database
    expenses = db.query(ExpenseDB).all()
    return expenses

@app.post("/expenses")
def add_expense(new_expense: Expense, db: Session = Depends(get_db)):
    # Convert Pydantic model to SQLAlchemy model
    db_expense = ExpenseDB(
        amount=new_expense.amount, 
        description=new_expense.description
    )
    # Add and commit to the database
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return {"message": "Expense added successfully", "expense": db_expense}

@app.get("/expenses/total")
def get_total(db: Session = Depends(get_db)):
    # Query all expenses and sum the amounts
    expenses = db.query(ExpenseDB).all()
    total = sum(exp.amount for exp in expenses)
    return {"total_expenses": total}

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    #1. Find the Expense by ID
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    
    #2. If not found, raise a 404 error
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    #3. Delete it and Save the database
    db.delete(expense)
    db.commit()
    
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
        # Use 'gemini-1.5-flash-latest' instead of just 'gemini-1.5-flash'
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(prompt)
        return {"analysis": response.text}
    except Exception as e:
        # Instantly return the exact error so Streamlit can display it
        print(f"BACKEND ERROR: {e}")
        return {"error": str(e)}
    
    return {"message": f"Expense {expense_id} deleted successfully."}