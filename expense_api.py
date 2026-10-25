from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List

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