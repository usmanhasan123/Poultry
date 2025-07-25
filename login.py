# import streamlit as st
# import app
# import feed_app
# import os

# username = os.getenv('login_username')
# password = os.getenv('login_password')

# def login(username, password):
#   user= st.text_input("username: ", key='user_key')
#   pswd= st.text_input("password: ", type='password', key='pass_key')

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
#   # st.write('username and password corrcet')
#   # subprocess.run(['python', 'app.py'])
#   tab1, tab2=st.tabs(["Daily Production", "Feed"])
#   with tab1:
#     app.main()
#   with tab2:
#     feed_app.main()


import streamlit as st
import app
import feed_app
import os

# Load credentials from environment
username = os.getenv('login_username')
password = os.getenv('login_password')

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'login_attempted' not in st.session_state:
    st.session_state.login_attempted = False

def login():
    user = st.text_input("Username: ", key='user_key')
    pswd = st.text_input("Password: ", type='password', key='pass_key')

    if st.button("Login"):
        st.session_state.login_attempted = True
        if user == username and pswd == password:
            st.session_state.logged_in = True
        else:
            st.error("Username or password incorrect")

# Main logic
if not st.session_state.logged_in:
    login()
else:
    st.success("Logged in successfully!")
    tab1, tab2 = st.tabs(["Daily Production", "Feed"])
    with tab1:
        app.main()
    with tab2:
        feed_app.main()
