import os
os.chdir('./')
import streamlit as st
import datetime
from get_and_upload_daily_production import production_class

def process(input_dict):
    obj=production_class(input_dict)
    obj.insert_in_daily_report()
    df=obj.fetch_daily_report()
    obj.update_daily_production_table(df)
    df2=obj.fetch_daily_production_table()
    return df, df2
    
def main():
    input_dict={}
    st.set_page_config(page_title="Daily Production Stats", page_icon=":robot:")
    st.header("Production Stats")
    date=st.date_input("date: ",value= datetime.date.today(),max_value= datetime.date.today(), key="date_input")
    remaining_balance_big_eggs=st.number_input("Remaining balance for large eggs: ", key='rem_large_key')
    remaining_balance_small_eggs=st.number_input("Remaining balance for small eggs: ", key='rem_small_key')
    input_dict['date']=date
    input_dict['remaining_balance_big_eggs']=remaining_balance_big_eggs
    input_dict['remaining_balance_small_eggs']=remaining_balance_small_eggs
    if 'inputs' not in st.session_state:
        st.session_state.inputs=1
    if 'show_warning' not in st.session_state:
        st.session_state.show_warning=False
    if 'process' not in st.session_state:
        st.session_state.process=False
        
    def add_inputs():
        st.session_state.inputs+=1
    def remove_inputs():
        st.session_state.inputs-=1
    
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
    
    if st.button("Submit"):
        dff=production_class.fetch_daily_report()
        if date in dff['date'].to_list():
            st.session_state['show_warning']=True
        else:
            if len(input_dict)>0:
                df, df2=process(input_dict)
                st.session_state['process']=True
            else:
                pass

    if st.session_state['show_warning']==True:            
        with st.dialog("Important Warning"):
            st.write("Records for this date already exist. Do you wish to continue?")
            if st.button("Yes, continue"):
                df, df2=process(input_dict)
                st.session_state['show_warning']=False
                st.session_state['process']=True
            elif st.button("No"):
                st.session_state['show_warning']=False
                st.session_state['process']=False
            else:
                pass
# initialize show warning to false and process to false
    if st.session_state['process']==True:
        colss=st.columns(2)
        colss[0].write(df)
        colss[1].write(df2)
    
    if st.button('Show report'):
        df=production_class.fetch_daily_report()
        df2=production_class.fetch_daily_production_table()
        colss=st.columns(2)
        colss[0].write(df)
        colss[1].write(df2)
    
        
    
        
