import streamlit as st
import requests

#Configure the page appearance
st.set_page_config(page_title="Expense Tracker", page_icon="💰")
st.title("💰 My Expense Tracker")

#The URL where the FastAPI backend is running
API_URL = "https://python-foundations-rho.vercel.app/api"

#Create a from for adding expenses:
st.subheader("Add a New Expense")
with st.form("add_expense_form"):
    #Create input widgets
    description = st.text_input("Description", placeholder="Enter Expense Description")
    amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0)
    #Submission
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        if description.strip() == "":
            st.error("Description cannot be empty.")
        else:
            #Send a POST request to the FastAPI backend
            new_expense = {"description": description, "amount": amount}
            response = requests.post(f"{API_URL}/expenses", json=new_expense, timeout=10)
            
            if response.status_code == 200:
                st.success("Expense Added Successfully!")
            else:
                st.error(f"Error: {response.status_code}")

st.divider()

#Display current expenses and total
st.subheader("Your Expenses")

#Send GET request to fetch the data
response = requests.get(f"{API_URL}/expenses", timeout=10)
total_response = requests.get(f"{API_URL}/expenses/total", timeout=10)

#Check if requests were successful
if response.status_code == 200 and total_response.status_code == 200:
    expenses_data = response.json()
    total_data = total_response.json()
    
    #Display the total in a metric box
    st.metric(label="Total Spend", value=f"₹{total_data['total_expenses']}")
    
    # AI Analysis Button
    if st.button("🤖 Analyze My Spending with AI"):
        with st.spinner("AI is thinking..."):
            ai_response = requests.get(f"{API_URL}/expenses/analyze", timeout=20)
            
            if ai_response.status_code == 200:
                response_data = ai_response.json()
                # Check if the AI worked or if the backend returned an error
                if "analysis" in response_data:
                    st.info(response_data["analysis"])
                else:
                    st.error(f"Backend Error: {response_data}")
            else:
                st.error("Failed to connect to the backend.")
    
    #Display list of expenses:
    if expenses_data:
        for exp in expenses_data:
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                st.write(f"**{exp['description']}** - ₹{exp['amount']} *(Category: {exp.get('category', 'N/A')})*")
            
            with col2:
                # 1. Extract the ID into a variable first
                expense_id = exp['id']
                
                # 2. Use the variable inside the f-string
                if st.button("Delete", key=f"del_{expense_id}"):
                    # 3. Use the variable here too
                    requests.delete(f"{API_URL}/expenses/{expense_id}", timeout=10)
                    st.rerun()
    else:
        st.info("No expenses added yet.")

else:
    st.error("Could not connect to the backend API. Is it running?")