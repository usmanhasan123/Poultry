import streamlit as st

if 'test' not in st.session_state:
  st.session_state.test=0
  
if st.button("Submit"):
  st.session_state.test=1

if st.session_state.test==1:
  st.write("this is a test case")
