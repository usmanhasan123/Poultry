# import streamlit as st
# import subprocess

# username = "root"
# password = "Oxygen123$"

# def login(username, password):
#   user= st.text_input("username: ", key='user_key')
#   pswd= st.text_input("password: ", key='pass_key')

#   if st.button("Login"):
#     if (user==username) and (pswd==password):
#       st.session_state['logged_in']=True
#       st.success("Logged in successfully")
#       # st.write('username and password corrcet')
#     else:
#       st.error("username or password incorrect")
      
# if 'logged_in' not in st.session_state:
#   st.session_state['logged_in']=False
  
# if st.session_state['logged_in']==False:
#   login(username, password)
# else:
#   st.write('username and password corrcet')
#   # subprocess.run(['python', 'app.py'])


import streamlit as st

# Hardcoded credentials (you can also store in st.secrets)
USERNAME = "admin"
PASSWORD = "1234"

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.title("Welcome to your app!")
    st.write("Only visible to logged-in users.")
