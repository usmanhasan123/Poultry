import os
os.chdir('./')
import streamlit as st
import datetime
from feed_class import feed_class

def main():
    input_dict={}
    st.set_page_config(page_title="Feed Logs", page_icon=":robot:")
    st.header("Feed Logs")
    date=st.date_input("date: ",value= datetime.date.today(), key="date_input")
    input_dict['date']=date
    if 'inputs_2' not in st.session_state:
        st.session_state.inputs_2=1
        
    def add_inputs():
        st.session_state.inputs_2+=1
    def remove_inputs():
        st.session_state.inputs_2-=1
    
    press=st.button("Add option", on_click=add_inputs)
    press1=st.button("Remove option", on_click=remove_inputs)
    for i in range(st.session_state.inputs_2):
        cols=st.columns(4)
        bori_amount=cols[0].number_input("amount (bori): ", key=f"bori_{i}")
        bilti_payment=cols[1].number_input("Bilti payment: ", key=f"bilti_{i}")
        paid_by=cols[1].selectbox("Paid by: ", ['Shahid', 'Siddiq'], key=f"paidby_{i}")
        dispatch_receipt=cols[3].number_input("dispatch receipt: ", key=f"dispatch_{i}")
        input_dict[f"{i+1}st feed"]={"bori_amount": bori_amount, "bilti_payment": bilti_payment, "paid_by":paid_by, "dispatch_receipt":dispatch_receipt}
    
    if st.button("Submit"):
        if len(input_dict)>0:
            obj=feed_class(input_dict)
            obj.insert_in_daily_report()
            df=obj.fetch_daily_report()
            obj.update_daily_production_table(df)
            df2=obj.fetch_daily_production_table()
        else:
            pass
        colss=st.columns(2)
        colss[0].write(df)
        colss[1].write(df2)
    
    if st.button('Show report'):
        df=production_class.fetch_daily_report()
        df2=production_class.fetch_daily_production_table()
        colss=st.columns(2)
        colss[0].write(df)
        colss[1].write(df2)
    
        
    
        
