from fastapi import FastAPI
from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    description: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Darshak! This is my first API."}