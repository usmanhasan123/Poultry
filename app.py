import os
os.chdir('./')
import streamlit as st
import datetime
from get_and_upload_daily_production import production_class
from debit_credit_class import debit_credit

def process(input_dict):
    obj=production_class(input_dict)
    obj.insert_in_daily_report()
    df=obj.fetch_daily_report()
    obj.update_daily_production_table(df)
    df2=obj.fetch_daily_production_table()
    return df, df2

def update_process(input_dict):
    obj=production_class(input_dict)
    obj.update_daily_report()
    df=obj.fetch_daily_report()
    obj.update_daily_production_table(df)
    df2=obj.fetch_daily_production_table()
    return df, df2
    
def main():
    st.set_page_config(page_title="Daily Production Stats", page_icon=":robot:")
    st.header("Production Stats")

    if 'inputs' not in st.session_state:
        st.session_state.inputs=1
    # if 'insert_report' not in st.session_state:
    #     st.session_state.insert_report=False
    # if 'update_report' not in st.session_state:
    #     st.session_state.update_report=False
    if 'show_warning' not in st.session_state:
        st.session_state.show_warning=False
    if 'process' not in st.session_state:
        st.session_state.process=False
    if 'log_balance' not in st.session_state:
        st.session_state.log_balance=False
    if 'update_balance' not in st.session_state:
        st.session_state.update_balance=False
        
    def add_inputs():
        st.session_state.inputs+=1
    def remove_inputs():
        st.session_state.inputs-=1

    tab1, tab2 = st.tabs(['Log daily report', 'Update daily_report'])
    with tab1:
        input_dict={}
        # st.session_state.insert_report=True
        date=st.date_input("date: ",value= datetime.date.today(),max_value= datetime.date.today(), key="date_input")
        remaining_balance_big_eggs=st.number_input("Remaining balance for large eggs: ", key='rem_large_key')
        remaining_balance_small_eggs=st.number_input("Remaining balance for small eggs: ", key='rem_small_key')
        input_dict['date']=date
        input_dict['remaining_balance_big_eggs']=remaining_balance_big_eggs
        input_dict['remaining_balance_small_eggs']=remaining_balance_small_eggs
        press=st.button("Add option", on_click=add_inputs)
        press1=st.button("Remove option", on_click=remove_inputs)
        for i in range(st.session_state.inputs):
            cols=st.columns(6)
            no_of_patty_gone=cols[0].number_input("no of patty gone: ", key=f"patty_{i}")
            egg_type=cols[1].selectbox("egg type: ", ['big', 'small'], key=f"type_{i}")
            rate=cols[2].number_input("rate: ", key=f"rate_{i}")
            cut=cols[3].number_input("cut: ", key=f"cut_{i}")
            open_or_closed=cols[4].selectbox("open or closed: ", ['open', 'closed'], key=f"open_{i}")
            party=cols[5].selectbox("party: ", ['Siddiq', 'Zulfi'], key=f"party_{i}")
            input_dict[f"{i+1}st party"]={"no_of_patty_gone": no_of_patty_gone, "egg_type": egg_type, "rate":rate, "cut":cut, "open_or_closed": open_or_closed, "party":party}
            
        @st.dialog("Important Warning")
        def warning():
            st.write("Records for this date already exist. Do you wish to continue?")
            col1, col2=st.columns(2)
            with col1:
                if st.button("Yes, continue"):
                    st.session_state.log_balance=True
                    st.session_state['process']=True
                    st.rerun()
            with col2:
                if st.button("No"):
                    st.session_state['process']=False
                    st.session_state.log_balance=False
                    st.rerun()
                
        if st.button("Submit", key='log_submit_key'):
            # if st.session_state.insert_report==True:
            dff=production_class.fetch_daily_report()
            if str(date) in dff['date'].to_list():
                st.session_state['show_warning']=True
            else:
                if len(input_dict)>0:
                    # df, df2=process(input_dict) # can remove this
                    st.session_state.log_balance=True
                    st.session_state['process']=True 

        if st.session_state['show_warning']==True:
            warning()
            st.session_state['show_warning']=False
    
        if st.session_state['process']==True:
            df, df2=process(input_dict)
            colss=st.columns(2)
            colss[0].write(df)
            colss[1].write(df2)
            st.session_state['process']=False

        if st.session_state['log_balance']==True:
            obj=debit_credit(input_dict)
            obj.insert_debit()
            st.session_state['log_balance']=False

    with tab2:
        input_dict={}
        # st.session_state.update_report=True
        options=st.multiselect("What details do you want to change?", ['date', 'no of patty gone', 'egg type', 'rate', 'cut', 'open or closed', 
                                                                      'Remaining balance for large eggs', 'Remaining balance for small eggs', 'party'], 
                               default=['date'])
        id=st.number_input('id: ', key='id_dets_rep')
        input_dict['id']=id
        if len(options)==0:
            cols=st.columns(1)
        else:
            cols=st.columns(len(options))
        for i, j in enumerate(options):
            if j=='date':
                date=cols[i].date_input("date: ", value=datetime.date.today(), max_value=datetime.date.today(), key='date_rep')
                input_dict['date']=date
            elif j=='no of patty gone':
                patty_gone=cols[i].number_input("no of patty gone", key='patty_gone_')
                input_dict['patty_gone']=patty_gone
            elif j=='egg type':
                egg_type=cols[i].selectbox("egg type: ",['big', 'small'], key="egg_type_")
                input_dict['type']=egg_type
            elif j=='rate':
                rate=cols[i].number_input("rate: ", key='rate_')
                input_dict['rate']=rate
            elif j=='cut':
                cut=cols[i].number_input("cut: ", key='cut_')
                input_dict['cut']=cut
            elif j=='open or closed':
                open_or_closed=cols[i].selectbox("open or closed: ",['open', 'closed'], key="open_close_")
                input_dict['open_or_closed']=open_or_closed
            elif j=='Remaining balance for large eggs':
                remaining_balance_big_eggs=cols[i].number_input("Remaining balance for large eggs: ", key='large_eggs_rem_')
                input_dict['remaining_balance_big_eggs']=remaining_balance_big_eggs
            elif j=='Remaining balance for small eggs':
                remaining_balance_small_eggs=cols[i].number_input("Remaining balance for small eggs: ", key='small_eggs_rem_')
                input_dict['remaining_balance_small_eggs']=remaining_balance_small_eggs
            elif j=='party':
                party=cols[i].selectbox("party: ",['Siddiq', 'Zulfi'], key='party_')
                input_dict['party']=party

        if st.button("Submit", key='update_submit_key'):
            st.session_state.update_balance=True
            # if st.session_state.update_report==True:
            if len(input_dict)>0:
                st.write("Hello")
                df, df2=update_process(input_dict)
                colss=st.columns(2)
                colss[0].write(df)
                colss[1].write(df2)
                # st.session_state['update_report']=False

        if st.session_state['update_balance']==True:
            obj=debit_credit(input_dict)
            obj.update_debit()
            st.session_state['update_balance']==False
        
    if st.button('Show report'):
        st.write("Hello")
        df=production_class.fetch_daily_report()
        df2=production_class.fetch_daily_production_table()
        colss=st.columns(2)
        colss[0].write(df)
        colss[1].write(df2)
    
        
    
        
