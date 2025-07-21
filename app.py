import streamlit as st

dictt={}
st.set_page_config(page_title="Daily Production Stats", page_icon=":robot:")
st.header("Production Stats")
date=st.text_input("date: ")
st.session_state.inputs=1
def add_inputs():
    st.session_state.inputs+=1
i=0
press=st.button("Click here if you want to put more options: ", on_click=add_inputs())
if press:
    st.write(i)
    i=i+1
    # cols=st.columns(6)
    # no_of_patty_gone=cols[0].text_input("no of patty gone: ", key=f"patty_{i}")
    # egg_type=cols[1].text_input("egg type: ", key=f"type_{i}")
    # rate=cols[2].text_input("rate: ", key=f"rate_{i}")
    # cut=cols[3].text_input("cut: ", key=f"cut_{i}")
    # open_or_closed=cols[4].text_input("open or closed: ", key=f"open_{i}")
    # party=cols[5].text_input("party: ", key=f"party_{i}")
    # dictt[f"{st.session_state.inputs}st party"]={"no_of_patty_gone": no_of_patty_gone, "egg_type": egg_type, "rate":rate, "cut":cut, "open_or_closed": open_or_closed, "party":party}


    
