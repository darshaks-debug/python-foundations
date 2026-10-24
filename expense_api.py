from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Expense(BaseModel):
    amount: float
    description: str

try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except FileNotFoundError:
    expenses = []

@app.get("/expenses")
def list_expenses():
    return expenses

@app.post("/expenses")
def add_expense(new_expense: Expense):
    try:
        # Use .dict() to be safe across different versions
        expense_dict = new_expense.dict() 
        expenses.append(expense_dict)
        
        with open("expenses.json", "w") as file:
            json.dump(expenses, file)
            
        return {"message": "Expense added successfully", "expense": expense_dict}
    except Exception as e:
        # If it crashes, this will print the EXACT reason to your terminal
        print(f"ERROR ADDING EXPENSE: {e}")
        return {"error": "Could not add expense"}

@app.get("/expenses/total")
def get_total():
    total = sum(exp["amount"] for exp in expenses)
    return {"total_expenses": total}