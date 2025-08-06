
import os
os.chdir('./')
import streamlit as st
import datetime
from debit_credit_class import debit_credit
import copy
    
def main():
    st.set_page_config(page_title="Balance Sheet", page_icon=":robot:")
    st.header("Balance Sheet")
    
    if 'insert_custom_debit' not in st.session_state:
        st.session_state.insert_custom_debit=False
    if 'update_custom_debit' not in st.session_state:
        st.session_state.update_custom_debit=False
    if 'insert_custom_credit' not in st.session_state:
        st.session_state.insert_custom_credit=False
    if 'update_custom_credit' not in st.session_state:
        st.session_state.update_custom_credit=False

    tab1, tab2 = st.tabs(['Log debit/credit', 'Update debit/credit'])

    with tab1:
        if st.button("Insert Debit"):
            st.session_state.insert_custom_debit=True
            st.session_state.insert_custom_credit=False
        if st.button("Insert Credit"):
            st.session_state.insert_custom_credit=True
            st.session_state.insert_custom_debit=False
    
        if st.session_state.insert_custom_debit==True:
            input_dict={}
            cols=st.columns(4)
            debit_date=cols[0].date_input("debit date: ",max_value= datetime.date.today(), key="debit_date_input")
            debit_descr=cols[1].text_input("debit description: ", key="deb_descr_input")
            debit_amount=cols[2].number_input("debit amount: ", key="deb_amount")
            party=cols[3].selectbox("Party: ", ['Siddiq', 'Masterfeed', 'Mudasir', 'Zulfi'], key="part_deb")
            input_dict['debit_date']=debit_date
            input_dict['debit_descr']=debit_descr
            input_dict['debit_amount']=debit_amount
            input_dict['party']=party
    
            if st.button("Submit", key='submit_key_ins_debit'):
                if len(input_dict)>0:
                    obj=debit_credit(copy.deepcopy(input_dict))
                    obj.insert_custom_debit()
                    df = obj.fetch_debit_credit_log()
                    st.write(df)
            # st.session_state.insert_custom_debit=False
            
        if st.session_state.insert_custom_credit==True:
            input_dict={}
            cols=st.columns(4)
            credit_date=cols[0].date_input("credit date: ",max_value= datetime.date.today(), key="credit_date_input")
            credit_descr=cols[1].text_input("credit description: ", key="cred_descr_input")
            credit_amount=cols[2].number_input("credit amount: ", key="cred_amount")
            party=cols[3].selectbox("Party: ", ['Siddiq', 'Masterfeed', 'Mudasir', 'Zulfi'], key="part_cred")
            input_dict['credit_date']=credit_date
            input_dict['credit_descr']=credit_descr
            input_dict['credit_amount']=credit_amount
            input_dict['party']=party
    
            if st.button("Submit", key='submit_key_ins_debit'):
                if len(input_dict)>0:
                    obj=debit_credit(copy.deepcopy(input_dict))
                    obj.insert_custom_credit()
                    # mf_list=['masterfeed', 'Masterfeed', 'MasterFeed', 'masterFeed', 'MASTERFEED', 'MF']
                    # mf_in_cred_descr=[i for i in mf_list if i in credit_descr]
                    # if mf_in_cred_descr:
                    # obj.insert_debit_for_masterfeed()
                    df = obj.fetch_debit_credit_log()
                    st.write(df)

    with tab2:
        if st.button("Update Debit"):
            st.session_state.update_custom_debit=True
            st.session_state.update_custom_credit=False
        if st.button("Update Credit"):
            st.session_state.update_custom_credit=True
            st.session_state.update_custom_debit=False
    
        if st.session_state.update_custom_debit==True:
            input_dict={}
            options=st.multiselect("What details do you want to change?", ['debit date', 'debit description', 'debit amount', 'Party'], 
                                   default=['debit date'])
            id=st.number_input('custom_debit_id: ', key='id_deb')
            input_dict['custom_debit_id']=id
            if len(options)==0:
                cols=st.columns(1)
            else:
                cols=st.columns(len(options))
            for i, j in enumerate(options):
                if j=='debit date':
                    date=cols[i].date_input("debit date: ", value=datetime.date.today(), max_value=datetime.date.today(), key='date_deb__')
                    input_dict['debit_date']=date
                elif j=='debit description':
                    deb_descr=cols[i].text_input("debit description", key='deb_descr_')
                    input_dict['debit_description']=deb_descr
                elif j=='debit amount':
                    debit_amount=cols[i].number_input("debit amount: ", key="deb_amount_")
                    input_dict['debit_amount']=debit_amount
                elif j=='Party':
                    party=cols[i].number_input("Party: ", key='party_upd_deb')
                    input_dict['party']=party
    
            if st.button("Submit", key='submit_key_upd_debit'):
                if len(input_dict)>0:
                    obj=debit_credit(copy.deepcopy(input_dict))
                    obj.update_custom_debit()
                    df = obj.fetch_debit_credit_log()
                    st.write(df)
            # st.session_state.update_custom_debit==False

        if st.session_state.update_custom_credit==True:
            input_dict={}
            options=st.multiselect("What details do you want to change?", ['credit date', 'credit description', 'credit amount', 'Party'], 
                                   default=['credit date'])
            id=st.number_input('custom_credit_id: ', key='id_cred')
            input_dict['custom_credit_id']=id
            if len(options)==0:
                cols=st.columns(1)
            else:
                cols=st.columns(len(options))
            for i, j in enumerate(options):
                if j=='credit date':
                    date=cols[i].date_input("credit date: ", value=datetime.date.today(), max_value=datetime.date.today(), key='date_cred__')
                    input_dict['credit_date']=date
                elif j=='credit description':
                    cred_descr=cols[i].text_input("credit description", key='cred_descr_')
                    input_dict['credit_description']=cred_descr
                elif j=='credit amount':
                    credit_amount=cols[i].number_input("credit amount: ", key="cred_amount_")
                    input_dict['credit_amount']=credit_amount
                elif j=='Party':
                    party=cols[i].number_input("Party: ", key='party_upd_cred')
                    input_dict['party']=party
    
            if st.button("Submit", key='submit_key_upd_debit'):
                if len(input_dict)>0:
                    obj=debit_credit(copy.deepcopy(input_dict))
                    obj.update_custom_credit()
                    df = obj.fetch_debit_credit_log()
                    st.write(df)
    
  
    
        
    
        
