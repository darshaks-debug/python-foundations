import streamlit as st
import requests

#Configure the page appearance
st.set_page_config(page_title="Expense Tracker", page_icon="💰")
st.title("💰 My Expense Tracker")

#The URL where the FastAPI backend is running
API_URL = "http://127.0.0.1:8000"

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
            response = requests.post(f"{API_URL}/expenses", json=new_expense)
            
            if response.status_code == 200:
                st.success("Expense Added Successfully!")
            else:
                st.error(f"Error: {response.status_code}")

st.divider()

#Display current expenses and total
st.subheader("Your Expenses")

#Send GET request to fetch the data
response = requests.get(f"{API_URL}/expenses")
total_response = requests.get(f"{API_URL}/expenses/total")

#Check if requess were successful
if response.status_code == 200 and total_response.status_code == 200:
    expenses_data = response.json()
    total_data = total_response.json()
    
    #Display the total in a metric box
    st.metric(label="Total Spend", value=f"₹{total_data['total_expenses']}")
    
    #Display list of expenses:
    if expenses_data:
        st.dataframe(expenses_data, use_container_width=True)
        st.bar_chart(expenses_data, x="description", y="amount")
    else:
        st.info("No expenses added yet.")

else:
    st.error("Could not connect to the backend API. Is it running?")