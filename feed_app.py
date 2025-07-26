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
    if 'is_masterfeed' not in st.session_state:
        st.session_state.is_masterfeed=False
    if 'is_callarrival' not in st.session_state:
        st.session_state.is_callarrival=True
        
    def add_inputs():
        st.session_state.inputs_2+=1
    def remove_inputs():
        st.session_state.inputs_2-=1

    tab1, tab2 = st.tabs(['Log feed dispatch', 'Update feed table'])
    with tab1:
        if st.checkbox("Log masterfeed?"):
            st.session_state.is_masterfeed=True
            date=st.date_input("date: ",value= datetime.date.today(), max_value= datetime.date.today(), key="date_feed_input_mas")
            input_dict['date']=date
            press=st.button("Add option", on_click=add_inputs, key='add_option_feed_mas')
            press1=st.button("Remove option", on_click=remove_inputs, key='remove_option_feed_mas')
            for i in range(st.session_state.inputs_2):
                cols=st.columns(4)
                bori_amount=cols[0].number_input("amount (bori): ", key=f"bori_mas_{i}")
                order_no=cols[1].text_input("order no. : ", key=f"order_mas_{i}")
                amount_paid=cols[1].number_input("amount paid : ", key=f"amount_mas_{i}")
                farm=cols[1].selectbox("Farm : ", ['Makhdoomia', 'Shahid', 'Usman'], key=f"farm_mas_{i}")
                input_dict[f"{i+1}st feed"]={"bori_amount": bori_amount, "order_no": order_no, "amount_paid":amount_paid, "farm":farm}
        else:
            st.session_state.is_masterfeed=False
            date=st.date_input("date: ",value= datetime.date.today(), max_value= datetime.date.today(), key="date_feed_input")
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
                if st.session_state.is_masterfeed==True:
                    obj=feed_class(input_dict)
                    obj.insert_in_feed_log_master()
                    df=obj.fetch_feed_log_master()
                else:
                    obj=feed_class(input_dict)
                    obj.insert_in_feed_log()
                    df=obj.fetch_feed_log()                    
            else:
                pass
            st.write(df)
    
    with tab2:
        if st.checkbox("Update masterfeed table?"):
            st.write("TBD")
        else:
            if st.button("Update car arrival"):
                st.session_state.is_callarrival=True
            if st.button("Update table details"):
                st.session_state.is_callarrival=False
                
            if st.session_state.is_callarrival==True:
                cols=st.columns(3)
                car_no=cols[0].number_input("car number: ", key="car_no")
                arrival_receipt=cols[1].text_input("arrival receipt: ", key="arr_rec")
                arrival_date=cols[2].date_input("arrival date: ",value= datetime.date.today(), key="date_arrival_input")
                input_dict['car_number']=car_no
                input_dict['arrival_receipt']=arrival_receipt
                input_dict['arrival_date']=arrival_date
            else:
                options=st.multiselect("What details do you want to change?", ['date', 'bori amount', 'bilti payment', 'paid by', 'dispatch receipt',
                                                                      'arrival date', 'arrival receipt', 'status'], default=['date'])
                st.number_input('car number: ', key='car_no_dets')
                if len(options)==0:
                    cols=st.columns(1)
                else:
                    cols=st.columns(len(options))
                for i, j in enumerate(options):
                    if j=='date':
                        date=cols[i].date_input("date: ", value=datetime.date.today(), max_value=datetime.date.today(), key='date_')
                    elif j=='paid by':
                        paid_by=cols[i].selectbox("Paid by: ", ['Shahid', 'Siddiq'], key=f"paidby_")
                    elif j=='dispatch receipt':
                        dispatch_receipt=cols[i].text_input("dispatch receipt: ", key=f"dispatch_")
                    elif j=='arrival date':
                        arrival_date=cols[i].date_input("arrival date: ", value=datetime.date.today(), key='date_arrival_')
                    elif j=='arrival receipt':
                        arrival_receipt=cols[i].text_input("arrival receipt: ", key=f"arrival_")
                    elif j=='status':
                        status=cols[i].selectbox("Status: ", ['DISPATCHED', 'ARRIVED'], key=f"status_")
                    elif j=='bori_amount':
                        bori_amount=cols[i].number_input("bori amount", key=f'bori_')
                    elif j=='bilti payment':
                        bilti=cols[i].number_input("bilti payment", key=f'bilti_')

        if st.button("Submit", key='submit_key_feed_update'):
            if len(input_dict)>0:
                # if st.sesison state ==True:
                obj=feed_class(input_dict)
                obj.update_feed_arrival()
                df=obj.fetch_feed_log()
                # else:
            # update the feed log according to selectboxes. make a func in feed_class for this
            else:
                pass
            st.write(df)

    
    if st.button('Show feed logs'):
        df_mudas=feed_class.fetch_feed_log()
        df_mas=feed_class.fetch_feed_log_master()
        col1, col2 = st.columns(2)
        col1.write(df_mudas)
        col2.write(df_mas)
    
        
    
        
