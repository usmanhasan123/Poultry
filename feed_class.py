# first insert into the raw daily_report table
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pyodbc
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

from get_and_upload_daily_production import production_class

class feed_class:
    def __init__(self, inputs):
        self.inputs=inputs
        if 'date' in self.inputs:
            self.inputs['date']=str(self.inputs['date'])
        self.feed_rate=5124.66
        # d1=self.inputs['date'].split('(')[1]
        # d1=d1.split(')')[0]
        # d1=d1.replace(', ', '-')
        # self.inputs['date']=pd.to_datetime(d1).strftime('%Y-%m-%d')
    @staticmethod
    def create_connection():
        conn=production_class.create_connection()
        return conn
        
    def insert_in_feed_log(self): # need to replace if date is repeated
        conn=self.create_connection()
        feed_df=self.fetch_feed_log()
        max_car_no=feed_df['car_number'].max()
        max_car_no=int(max_car_no) # so that it is compatible with mysql
        max_car_no=max_car_no+1
        # self.inputs['date']=self.inputs['date'].strftime("%Y-%m-%d")
        input_keys=[]
        for i in self.inputs:
            if type(self.inputs[i])==dict:
                total_amount=self.feed_rate*self.inputs[i]['bori_amount']
                amount_paid=total_amount - self.inputs[i]['bilti_payment']
                self.inputs[i]['total_amount'] = total_amount
                self.inputs[i]['amount_paid'] = amount_paid
                self.inputs[i]['status']='DISPATCHED'
                self.inputs[i]['car_number']=max_car_no
                input_keys.append(i)
                recs=[]
                max_car_no=max_car_no+1
        
        for i in input_keys:
            params=self.inputs[i]
            a=list(params.values())
            for j in self.inputs:
                if j not in input_keys:
                    a.append(self.inputs[j])
            recs.append(tuple(a))
        
        recs2=[]
        for i in recs:
            k=1
            dictt={}
            for j in i:
                dictt[str(k)]=j
                k=k+1
            recs2.append(dictt)
    
        query="insert into feed_log (amount, bilti_payment, paid_by, dispatch_receipt, total_amount, amount_paid, status, car_number, date) \
        values (:1, :2, :3, :4, :5, :6, :7, :8, :9)"
        with conn.connect() as con:
            con.execute(text(query), recs2)
            con.commit()

    def update_feed_arrival():
        conn=self.create_connection()
        query = 'update feed_log set arrival_date=:1, arrival_receipt=:2, status=:3 where car_number=:4'
        recs=[{'1': self.inputs['arrival_date'], '2': self.inputs['arrival_receipt'], '3': 'ARRIVED', '4': self.inputs['car_number']}]

        with conn.connect() as con:
            con.execute(text(query), recs)
            con.commit()

    @staticmethod
    def fetch_feed_log():
        conn=production_class.create_connection()
        query="select * from feed_log"
        df=pd.read_sql(text(query), conn)
        return df
