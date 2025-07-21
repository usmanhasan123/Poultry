import streamlit as st

dictt={}
st.set_page_config(page_title="Daily Production Stats")

date=st.text_input("date: ")
st.session_state.inputs=1
def add_inputs():
    st.session_state.inputs=st.session_state.inputs+1

press=st.button("Click here if you want to put more options: ", on_click=add_inputs)
for i in range(st.session_state.inputs):
    no_of_patty_gone=st.text_input("no of patty gone: ", key=f"patty_{i}")
    egg_type=st.text_input("egg type: ", key=f"type_{i}")
    rate=st.text_input("rate: ", key=f"rate_{i}")
    cut=st.text_input("cut: ", key=f"cut_{i}")
    open_or_closed=st.text_input("open or closed: ", key=f"open_{i}")
    party=st.text_input("party: ", key=f"party_{i}")
    dictt[f"{i}st party"]={"no_of_patty_gone": no_of_patty_gone, "egg_type": egg_type, "rate":rate, "cut":cut, "open_or_closed": open_or_closed, "party":party}


    