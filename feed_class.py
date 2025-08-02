# first insert into the raw daily_report table
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pyodbc
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
import json
import streamlit as st

from get_and_upload_daily_production import production_class

class feed_class:
    def __init__(self, inputs):
        self.inputs=inputs
        if 'date' in self.inputs:
            self.inputs['date']=str(self.inputs['date'])
        # self.feed_rate=5124.66
        # d1=self.inputs['date'].split('(')[1]
        # d1=d1.split(')')[0]
        # d1=d1.replace(', ', '-')
        # self.inputs['date']=pd.to_datetime(d1).strftime('%Y-%m-%d')
    @staticmethod
    def create_connection():
        conn=production_class.create_connection()
        return conn
        
    @staticmethod
    def extract_feed_rate():
        conn=production_class.create_connection()
        query="select * from feed_rate"
        df=pd.read_sql(text(query), conn)
        return df
        
    def insert_in_feed_log(self): # need to replace if date is repeated
        conn=self.create_connection()
        feed_df=self.fetch_feed_log()
        feed_rate = self.extract_feed_rate()
        feed_rate=feed_rate[feed_rate['feed_provider']=='Mudasir']
        max_car_no=feed_df['car_number'].max()
        if 'int' in str(type(max_car_no)):
            max_car_no=int(max_car_no) # so that it is compatible with mysql
            max_car_no=max_car_no+1
        else:
            max_car_no=53
            max_car_no=int(max_car_no)
        # self.inputs['date']=self.inputs['date'].strftime("%Y-%m-%d")
        input_keys=[]
        for i in self.inputs:
            total_amount=0
            if type(self.inputs[i])==dict:
                for j in self.inputs[i]['feed_bifurcation'].keys():
                    xx=feed_rate[feed_rate['id']==int(feed_rate[feed_rate['product_name']==j]['id'].max())]
                    ratee = (xx['rate'].iloc[0] - (xx['rate'].iloc[0] * (xx['discount']/100))) + xx['gst_per_bag'].iloc[0]
                    amount_for_feed=ratee.iloc[0]*self.inputs[i]['feed_bifurcation'][j]
                    total_amount=total_amount+amount_for_feed
                # total_amount=self.feed_rate*self.inputs[i]['bori_amount']
                amount_paid=total_amount - self.inputs[i]['bilti_payment']
                self.inputs[i]['total_amount'] = total_amount
                self.inputs[i]['amount_paid'] = amount_paid
                self.inputs[i]['status']='DISPATCHED'
                self.inputs[i]['car_number']=max_car_no
                self.inputs[i]['feed_bifurcation']=json.dumps(self.inputs[i]['feed_bifurcation'])
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
        # query_del="delete from feed_log where car_number=:1"
        # rec_del=
        query="insert into feed_log (amount, bilti_payment, paid_by, dispatch_receipt, feed_bifurcation, total_amount, amount_paid, status, car_number, date) \
        values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"
        with conn.connect() as con:
            con.execute(text(query), recs2)
            con.commit()

    def insert_in_feed_log_master(self): # need to replace if date is repeated
        conn=self.create_connection()
        feed_df=self.fetch_feed_log_master()
        
        max_id=feed_df['id'].max()
        max_id=int(max_id) # so that it is compatible with mysql
        max_id=max_id+1
        
        input_keys=[]
        for i in self.inputs:
            if type(self.inputs[i])==dict:
                self.inputs[i]['id']=max_id
                input_keys.append(i)
                max_id=max_id+1
        recs=[]

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
    
        query="insert into feed_log_master (amount, order_no, amount_paid, farm, id, date) \
        values (:1, :2, :3, :4, :5, :6)"
        with conn.connect() as con:
            con.execute(text(query), recs2)
            con.commit()

    def update_feed_arrival(self):
        conn=self.create_connection()
        query = 'update feed_log set arrival_date=:1, arrival_receipt=:2, status=:3 where car_number=:4'
        recs=[{'1': self.inputs['arrival_date'], '2': self.inputs['arrival_receipt'], '3': 'ARRIVED', '4': self.inputs['car_number']}]

        with conn.connect() as con:
            con.execute(text(query), recs)
            con.commit()

    def update_feed_table(self):
        conn=self.create_connection()
        dff=feed_class.fetch_feed_log()
        df=dff[dff['car_number']==self.inputs['car_number']]
        feed_rate = self.extract_feed_rate()
        feed_rate=feed_rate[feed_rate['feed_provider']=='Mudasir']
        # columns_to_update=self.inputs.keys()
        total_amount=0
        st.write(self.inputs['feed_bifurcation'])
        st.write(type(self.inputs['feed_bifurcation'])=='dict')
        if 'feed_bifurcation' in self.inputs:
            for i,j in enumerate(self.inputs['feed_bifurcation'].keys()):
                xx=feed_rate[feed_rate['id']==int(feed_rate[feed_rate['product_name']==j]['id'].max())]
                ratee = (xx['rate'].iloc[0] - (xx['rate'].iloc[0] * (xx['discount']/100))) + xx['gst_per_bag'].iloc[0]
                amount_for_feed=ratee.iloc[0]*self.inputs['feed_bifurcation'][j]
                total_amount=total_amount+amount_for_feed
        else:
            for i,j in json.loads(df['feed_bifurcation'].iloc[0]).keys():
                xx=feed_rate[feed_rate['id']==int(feed_rate[feed_rate['product_name']==j]['id'].max())]
                ratee = (xx['rate'].iloc[0] - (xx['rate'].iloc[0] * (xx['discount']/100))) + xx['gst_per_bag'].iloc[0]
                amount_for_feed = ratee.iloc[0]*json.loads(df['feed_bifurcation'].iloc[0])[j]
                total_amount=total_amount+amount_for_feed

        if 'bilti_payment' in self.inputs:
            amount_paid = total_amount - self.inputs['bilti_payment']
        else:
            amount_paid = total_amount - float(df['bilti_payment'].iloc[0])
        self.inputs['total_amount'] = total_amount
        self.inputs['amount_paid'] = amount_paid
        self.inputs['feed_bifurcation']=json.dumps(self.inputs['feed_bifurcation'])
        columns_to_update=self.inputs.keys()
        set_clause = ', '.join(f"{i}=:{i}" for i in columns_to_update if i != 'car_number')
        query = f"update feed_log set {set_clause} where car_number=:car_number"
        recs=self.inputs
        # recs=[{'1': self.inputs['arrival_date'], '2': self.inputs['arrival_receipt'], '3': 'ARRIVED', '4': self.inputs['car_number']}]

        with conn.connect() as con:
            con.execute(text(query), recs)
            con.commit()

    def update_feed_table_master(self):
        conn=self.create_connection()
        columns_to_update=self.inputs.keys()
        set_clause = ', '.join(f"{i}=:{i}" for i in columns_to_update if i != 'id')
        query = f"update feed_log_master set {set_clause} where id=:id"
        recs=self.inputs
        # recs=[{'1': self.inputs['arrival_date'], '2': self.inputs['arrival_receipt'], '3': 'ARRIVED', '4': self.inputs['car_number']}]

        with conn.connect() as con:
            con.execute(text(query), recs)
            con.commit()
            
    @staticmethod
    def fetch_feed_log():
        conn=production_class.create_connection()
        query="select * from feed_log order by car_number asc"
        df=pd.read_sql(text(query), conn)
        return df
    @staticmethod
    def fetch_feed_log_master():
        conn=production_class.create_connection()
        query="select * from feed_log_master order by date asc"
        df=pd.read_sql(text(query), conn)
        return df
