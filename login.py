import streamlit as st
import app

username = "root"
password = "Oxygen123$"

def login(username, password):
  user= st.text_input("username: ", key='user_key')
  pswd= st.text_input("password: ", type='password', key='pass_key')

  if st.button("Login"):
    if (user==username) and (pswd==password):
      st.session_state['logged_in']=True
      st.success("Logged in successfully")
      # st.write('username and password corrcet')
    else:
      st.error("username or password incorrect")
      
if 'logged_in' not in st.session_state:
  st.session_state['logged_in']=False
  
if st.session_state['logged_in']==False:
  login(username, password)
else:
  # st.write('username and password corrcet')
  # subprocess.run(['python', 'app.py'])
  tab1=st.tabs(["Daily Production"])
  tab1.write("Contents for tab1")
  # app.main()
