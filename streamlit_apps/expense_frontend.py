import streamlit as st
import requests

st.set_page_config(page_title="Expense Tracker", page_icon="💰")
st.title("💰 My Expense Tracker")

# Use the live Railway backend
API_URL = "https://python-foundations-production.up.railway.app"

# --- 1. SESSION STATE SETUP ---
# We need to remember the token across page reloads
if "token" not in st.session_state:
    st.session_state.token = None

# --- 2. AUTHENTICATION SCREEN ---
if st.session_state.token is None:
    st.subheader("Welcome! Please Login or Register")
    
    # Create two tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            # FastAPI's OAuth2 expects form data, not JSON
            login_data = {"username": login_user, "password": login_pass}
            response = requests.post(f"{API_URL}/token", data=login_data)
            
            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.success("Logged in successfully!")
                st.rerun() # Refresh the page to show the main app
            else:
                st.error("Invalid username or password.")

    with tab2:
        reg_user = st.text_input("Choose Username", key="reg_user")
        reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        
        if st.button("Register"):
            reg_data = {"username": reg_user, "password": reg_pass}
            response = requests.post(f"{API_URL}/register", json=reg_data)
            
            if response.status_code == 200:
                st.success("User created! Please go to the Login tab.")
            else:
                st.error("Username already exists.")

# --- 3. THE MAIN APP (Only shows if logged in) ---
else:
    # Create the headers dictionary with the token
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Logout Button in the sidebar
    with st.sidebar:
        st.write(f"You are logged in.")
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()

    st.subheader("Add a New Expense")
    with st.form("add_expense_form"):
        description = st.text_input("Description", placeholder="Enter Expense Description")
        amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0)
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            if description.strip() == "":
                st.error("Description cannot be empty.")
            else:
                new_expense = {"description": description, "amount": amount}
                # SEND THE HEADERS!
                response = requests.post(f"{API_URL}/expenses", json=new_expense, headers=headers)
                
                if response.status_code == 200:
                    st.success("Expense Added Successfully!")
                    st.rerun() # Refresh to show the new item
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

    st.divider()
    st.subheader("Your Expenses")

    # Fetch expenses AND total (with headers)
    response = requests.get(f"{API_URL}/expenses", headers=headers)
    total_response = requests.get(f"{API_URL}/expenses/total", headers=headers)

    if response.status_code == 200 and total_response.status_code == 200:
        expenses_data = response.json()
        total_data = total_response.json()
        
        st.metric(label="Total Spend", value=f"₹{total_data['total_expenses']}")
        
        # AI Analysis Button
        if st.button("🤖 Analyze My Spending with AI"):
            with st.spinner("AI is thinking..."):
                ai_response = requests.get(f"{API_URL}/expenses/analyze", headers=headers, timeout=20)
                
                if ai_response.status_code == 200:
                    response_data = ai_response.json()
                    if "analysis" in response_data:
                        st.info(response_data["analysis"])
                    else:
                        st.error(f"Backend Error: {response_data}")
                else:
                    st.error("Failed to connect to the backend.")
        
        # Display Expenses
        if expenses_data:
            for exp in expenses_data:
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.write(f"**{exp['description']}** - ₹{exp['amount']} *(Category: {exp.get('category', 'N/A')})*")
                
                with col2:
                    expense_id = exp['id']
                    # SEND THE HEADERS!
                    if st.button("Delete", key=f"del_{expense_id}"):
                        requests.delete(f"{API_URL}/expenses/{expense_id}", headers=headers)
                        st.rerun()
        else:
            st.info("No expenses added yet.")
    else:
        st.error("Could not fetch expenses. Your session may have expired. Please log out and log back in.")