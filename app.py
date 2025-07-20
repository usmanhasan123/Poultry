import streamlit as st

dictt={}
st.set_page_config(page_title="Daily Production Stats")

date=st.text_inputs("date: ")
st.session_state.inputs=1
def add_input():
    st.session_state.inputs=st.session_state.inputs+1

press=st.button("Click here if you want to put more options: ", on_click=add_inputs)
for i in st.session_state.inputs:
    no_of_patty_gone=st.text_inputs("no of patty gone: ", key=f"patty_{i}")
    egg_type=st.text_inputs("egg type: ", key=f"type_{i}"))
    rate=st.text_inputs("rate: ", key=f"rate_{i}"))
    cut=st.text_inputs("cut: ", key=f"cut_{i}"))
    open_or_closed=st.text_inputs("open or closed: ", key=f"open_{i}"))
    party=st.text_inputs("party: ", key=f"party_{i}"))
    dictt[f"{i}st party"]={"no_of_patty_gone": no_of_patty_gone, "egg_type": egg_type, "rate":rate, "cut":cut, "open_or_closed": open_or_closed, "party":party}


    