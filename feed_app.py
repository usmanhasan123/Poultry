import os
os.chdir('./')
import streamlit as st
import datetime
from feed_class import feed_class

def main():
    input_dict={}
    st.set_page_config(page_title="Feed Logs", page_icon=":robot:")
    st.header("Feed Logs")
    
    if 'inputs_2' not in st.session_state:
        st.session_state.inputs_2=1
        
    def add_inputs():
        st.session_state.inputs_2+=1
    def remove_inputs():
        st.session_state.inputs_2-=1

    tab1, tab2 = st.tabs(['Log feed dispatch', 'Log feed arrival'])
    with tab1:
        date=st.date_input("date: ",value= datetime.date.today(), key="date_feed_input")
        input_dict['date']=date
        press=st.button("Add option", on_click=add_inputs, key='add_option_feed')
        press1=st.button("Remove option", on_click=remove_inputs, key='remove_option_feed')
        for i in range(st.session_state.inputs_2):
            cols=st.columns(4)
            bori_amount=cols[0].number_input("amount (bori): ", key=f"bori_{i}")
            bilti_payment=cols[1].number_input("Bilti payment: ", key=f"bilti_{i}")
            paid_by=cols[1].selectbox("Paid by: ", ['Shahid', 'Siddiq'], key=f"paidby_{i}")
            dispatch_receipt=cols[3].text_input("dispatch receipt: ", key=f"dispatch_{i}")
            input_dict[f"{i+1}st feed"]={"bori_amount": bori_amount, "bilti_payment": bilti_payment, "paid_by":paid_by, "dispatch_receipt":dispatch_receipt}
            
        if st.button("Submit", key='submit_key_feed'):
            if len(input_dict)>0:
                obj=feed_class(input_dict)
                obj.insert_in_feed_log()
                df=obj.fetch_feed_log()
            else:
                pass
            st.write(df)
    
    with tab2:
        cols=st.columns(3)
        car_no=cols[0].number_input("car number: ", key=f"car_no")
        arrival_receipt=cols[1].text_input("arrival receipt: ", key=f"arr_rec")
        arrival_date=cols[2].date_input("arrival date: ",value= datetime.date.today(), key="date_arrival_input")
        input_dict['car_number']=car_no
        input_dict['arrival_receipt']=arrival_receipt
        input_dict['arrival_date']=arrival_date

        if st.button("Submit", key='submit_key_feed_update'):
            if len(input_dict)>0:
                obj=feed_class(input_dict)
                obj.update_feed_arrival()
                df=obj.fetch_feed_log()
            else:
                pass
            st.write(df)

    
    if st.button('Show feed logs'):
        df=feed_class.fetch_feed_log()
        st.write(df)
    
        
    
        
