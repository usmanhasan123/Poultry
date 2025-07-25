# import streamlit as st

# if 'test' not in st.session_state:
#   st.session_state.test=0
  
# if st.button("Submit"):
#   st.session_state.test=1

# if st.session_state.test==1:
#   st.write("this is a test case")

# import streamlit as st

# if "show_dialog" not in st.session_state:
#     st.session_state.show_dialog = False

# # Trigger the dialog
# if st.button("Show Warning"):
#     st.session_state.show_dialog = True
# def keyy():
#   st.write('this is a test case')
# # Define the dialog box
# if st.session_state.show_dialog:
#     st.dialog("Important Warning", keyy)
import streamlit as st

@st.dialog("My Dialog")
def show_my_dialog():
    st.write("This content is displayed in the dialog.")
    if st.button("Close Dialog"):
      st.rerun()# Example of closing the dialog

if st.button("Open Dialog"):
    show_my_dialog() 
