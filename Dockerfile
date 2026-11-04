# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first (this makes rebuilding faster)
COPY api/requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your backend code into the container
COPY expense_api.py .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Command to run the application
CMD ["uvicorn", "expense_api:app", "--host", "0.0.0.0", "--port", "8000"]