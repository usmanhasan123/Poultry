import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pyodbc
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

from get_and_upload_daily_production import production_class

class debit_credit:
    def __init__(self, inputs):
        self.inputs=inputs
        if 'date' in self.inputs:
            self.inputs['date']=str(self.inputs['date'])

    @staticmethod
    def create_connection():
        conn=production_class.create_connection()
        return conn

    def insert_debit(self):
        conn=self.create_connection()
        dff=self.fetch_daily_report()
        final_input={}
        party_count={}
        input_keys=[]
        final_input['debit_date']=self.inputs['date']
        for i in self.inputs:
            if type(self.inputs[i])==dict:
                patty_amount=self.inputs[i]['rate'] - self.inputs[i]['cut']
                no_of_patty_gone=self.inputs[i]['no_of_patty_gone']
                final_input['debit_description'] = f"{no_of_patty_gone} x {patty_amount}"
                final_input['debit_amount'] = no_of_patty_gone*patty_amount
                final_input['party'] = self.inputs[i]['party']
                final_input['week'] = int(pd.to_datetime(self.inputs['date']).strftime("%W"))
                final_input['credit_amount'] = 0
                
                if final_input['party'] not in party_count:
                    party_count[final_input['party']] = 0
                else:
                    party_count[final_input['party']]=party_count[final_input['party']]+1

                ids=dff[(dff['debit_date']==self.inputs['date']) & (dff['party']==self.inputs['party'])]['id'].to_list()

                final_input['report_id'] = ids[party_count[final_input['party']]]
    
                query = "insert into debit_credit_table (debit_date, debit_description, debit_amount, party, week, credit_amount, report_id) \
                values (:debit_date, :debit_description, :debit_amount, :party, :week, :credit_amount, :report_id)"
                with conn.connect() as con:
                    con.execute(text(query), final_input)
                    con.commit()


    @staticmethod
    def fetch_debit_credit_log():
        conn=production_class.create_connection()
        query="select * from debit_credit_table"
        df=pd.read_sql(text(query), conn)
        return df

            


                
