

import streamlit as st

# Initialize user credentials in session state if not already done
if "user_credentials" not in st.session_state:
    st.session_state["user_credentials"] = {
        "Himesh": "12345",
        "Alice": "password1",
        "Bob": "password2",
        "Charlie": "password3"
    }

# Function to verify login credentials
def verify_login(username, password):
    user_credentials = st.session_state["user_credentials"]
    if username in user_credentials and user_credentials[username] == password:
        return True
    return False

# Function to handle user sign-up
def handle_signup(username, password, confirm_password):
    user_credentials = st.session_state["user_credentials"]
    if username in user_credentials:
        return False, "Username already exists. Please choose a different username."
    if len(username.strip()) == 0 or len(password.strip()) == 0 or len(confirm_password.strip()) == 0:
        return False, "Username, Password, and Confirm Password cannot be empty."
    if password != confirm_password:
        return False, "Passwords do not match. Please try again."
    user_credentials[username] = password
    st.session_state["user_credentials"] = user_credentials
    return True, "Sign-Up successful! You can now log in."

# Function to clear session state
def clear_session():
    st.session_state["authenticated"] = False
    st.session_state["user"] = None

# Display Login Form
def display_login_form():
    st.text_input("Username:", key="login_user")
    st.text_input("Password:", key="login_passwd", type="password")
    if st.button("Login"):
        username = st.session_state.get("login_user", "").strip()
        password = st.session_state.get("login_passwd", "").strip()
        if verify_login(username, password):
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid username or password.")

# Display Sign-In Form (includes Confirm Password for sign-up)
def display_signin_form():
    st.text_input("Username:", key="signin_user")
    st.text_input("Password:", key="signin_passwd", type="password")
    st.text_input("Confirm Password:", key="confirm_passwd", type="password")  # Confirm Password Field
    if st.button("Sign In"):  # Button name is "Sign In"
        username = st.session_state.get("signin_user", "").strip()
        password = st.session_state.get("signin_passwd", "").strip()
        confirm_password = st.session_state.get("confirm_passwd", "").strip()  # Fetch Confirm Password

        if username in st.session_state["user_credentials"]:  # Check if the user exists
            # If user exists, proceed to log in
            if verify_login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["user"] = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Incorrect password. Please try again.")
        else:
            # If user doesn't exist, create a new account
            success, message = handle_signup(username, password, confirm_password)
            if success:
                st.success(message)
            else:
                st.error(message)

# Main App Logic
def main():
    st.title("Authenticated Power BI Dashboard Integration with Streamlit")
    
    # Check if user is already authenticated
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # Show Login and Sign-In options
        st.header("Login or Sign In")
        option = st.radio("Choose an option:", ["Login", "Sign In"])
        
        if option == "Login":
            display_login_form()
        elif option == "Sign In":  # Calls the updated Sign-In form
            display_signin_form()  
    else:
        # User is authenticated
        st.success(f"Welcome, {st.session_state['user']}!")
        if st.button("Logout"):
            clear_session()
            st.success("You have been logged out. Please refresh the page to log in again.")
        else:
            # Display dashboard description
            st.write("This app integrates a Power BI dashboard within a Streamlit web application. Explore the visualizations and gain insights directly from the embedded Power BI dashboard.")

            # Embed Power BI Dashboard
            power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiZjY1MjljZGMtMzU5MC00YTU3LThhYjAtZTJmOGUxY2NhNjNiIiwidCI6ImQ4MDI5Y2VmLTJhZTEtNDY5Ni1iYWIxLTI4NmU4ZWUxMjQ0ZCJ9"
            st.components.v1.iframe(src=power_bi_url, width=1000, height=600, scrolling=True)

            # Footer
            st.write("---")
            st.write("Developed with ❤️ using Streamlit and Power BI")


if __name__ == "__main__":
    main()



    
