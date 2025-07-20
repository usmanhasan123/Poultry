# first insert into the raw daily_report table
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pyodbc

class production_class:
    def __init__(self, inputs):
        self.inputs=inputs
    @staticmethod
    def create_connection():
        conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-GCHR40U;'
        'DATABASE=poultry_db;'
        'Trusted_Connection=yes;'
        )
        return conn
        
    def insert_in_daily_report(self, conn): # need to replace if date is repeated
        input_keys=[]
        for i in self.inputs:
            if type(self.inputs[i])==dict:
                input_keys.append(i)
        recs=[]
    
        for i in input_keys:
            params=self.inputs[i]
            a=list(params.values())
            for j in self.inputs:
                if j not in input_keys:
                    a.append(self.inputs[j])
            recs.append(tuple(a))
    
        query="insert into daily_report (patty_gone, type, rate, cut, open_or_closed, party, date, remaining_balance_big_eggs, remaining_balance_small_eggs) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor=conn.cursor()
        cursor.executemany(query, recs)
        cursor.commit()

    @staticmethod
    def fetch_daily_report(conn):
        query="select * from daily_report"
        cursor=conn.cursor()
        cursor.execute(query)
    
        data = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        df=pd.DataFrame.from_records(data, columns=columns)
        return df
    
    def update_daily_production_table(self, conn, df):
        date_to_update=self.inputs['date']
        df['remaining_balance'] = df['remaining_balance_big_eggs'] + df['remaining_balance_small_eggs']
        df1=df[df['date']==date_to_update]
        df2=df1.groupby('date').agg(no_of_patty_gone=('patty_gone', 'sum'), rem_balance=('remaining_balance', 'mean')).reset_index() # df2 shouldhave 1 row
        
        x=pd.to_datetime(date_to_update) - timedelta(days=1)
        last_day=x.strftime("%Y-%m-%d")
        df_last_day=df[df['date']==last_day]
    
        today_production=df2['no_of_patty_gone'].iloc[0] + df2['rem_balance'].iloc[0]-df_last_day['remaining_balance'].iloc[0]
    
        recs=[(date_to_update, today_production)]
    
        query="insert into daily_production (date, production) values (?, ?)"
    
        cursor=conn.cursor()
        cursor.executemany(query, recs)
        cursor.commit()

    @staticmethod
    def fetch_daily_production_table(conn):
        query="select * from daily_production"
        cursor=conn.cursor()
        cursor.execute(query)
    
        data = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        df=pd.DataFrame.from_records(data, columns=columns)
        return df