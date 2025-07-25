# import streamlit as st

# if 'test' not in st.session_state:
#   st.session_state.test=0
  
# if st.button("Submit"):
#   st.session_state.test=1

# if st.session_state.test==1:
#   st.write("this is a test case")

import streamlit as st

if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False

# Trigger the dialog
if st.button("Show Warning"):
    st.session_state.show_dialog = True

# Define the dialog box
if st.session_state.show_dialog:
    with st.dialog("Important Warning"):
        st.warning("This action will overwrite existing records. Do you want to continue?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, continue"):
                st.session_state.show_dialog = False
                st.success("Process executed")
                # Your function call here
        with col2:
            if st.button("Cancel"):
                st.session_state.show_dialog = False
