import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pyodbc
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

from get_and_upload_daily_production import production_class
from feed_class import feed_class

class debit_credit:
    def __init__(self, inputs):
        self.inputs=inputs
        if 'date' in self.inputs:
            self.inputs['date']=str(self.inputs['date'])
        # self.feed_rate=5124.66

    @staticmethod
    def create_connection():
        conn=production_class.create_connection()
        return conn

    def insert_debit(self): # after eggs gone
        conn=self.create_connection()
        dff=self.fetch_debit_credit_log()
        max_id=dff['report_id'].max()
        # remove this if statement later. replace with:
        #  max_id=int(max_id) # so that it is compatible with mysql
        # max_id=max_id+1
        if 'int' in str(type(max_id)):
            max_id=int(max_id) # so that it is compatible with mysql
            max_id=max_id+1
        else:
            max_id=19
            max_id=int(max_id)
        
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
                
                final_input['report_id'] = max_id
                max_id=max_id+1
                # if final_input['party'] not in party_count:
                #     party_count[final_input['party']] = 0
                # else:
                #     party_count[final_input['party']]=party_count[final_input['party']]+1
                # ids=dff[(dff['date']==self.inputs['date']) & (dff['party']==self.inputs[i]['party'])]['id'].to_list()
                # final_input['report_id'] = ids[party_count[final_input['party']]]
    
                query = "insert into debit_credit_table (debit_date, debit_description, debit_amount, party, week, credit_amount, report_id) \
                values (:debit_date, :debit_description, :debit_amount, :party, :week, :credit_amount, :report_id)"
                with conn.connect() as con:
                    con.execute(text(query), final_input)
                    con.commit()

    def update_debit(self): # for eggs gone
        conn=self.create_connection()
        dff=production_class.fetch_daily_report()
        df=dff[dff['id']==self.inputs['id']]
        final_input={}
        if 'patty_gone' in self.inputs.keys():
            no_of_patty_gone = self.inputs['patty_gone']
        else:
            no_of_patty_gone=int(df['patty_gone'].iloc[0])

        if 'rate' in self.inputs.keys():
            rate = self.inputs['rate']
        else:
            rate=float(df['rate'].iloc[0])

        if 'cut' in self.inputs.keys():
            cut = self.inputs['cut']
        else:
            cut=float(df['cut'].iloc[0])
        
        if 'date' in self.inputs.keys():
            final_input['debit_date'] = self.inputs['date']
            final_input['week'] = int(pd.to_datetime(self.inputs['date']).strftime("%W"))
        elif 'party' in self.inputs.keys():
            final_input['party']=self.inputs['party']
        patty_amount = rate-cut
        debit_amount=no_of_patty_gone*patty_amount
        final_input['debit_description'] = f"{no_of_patty_gone} x {patty_amount}"
        final_input['debit_amount'] = debit_amount
        final_input['report_id'] = self.inputs['id']
        columns_to_update=final_input.keys()
        set_clause = ', '.join(f"{i}=:{i}" for i in columns_to_update if i != 'report_id')
        query = f"update debit_credit_table set {set_clause} where report_id=:report_id"
        # recs=[{'1': self.inputs['arrival_date'], '2': self.inputs['arrival_receipt'], '3': 'ARRIVED', '4': self.inputs['car_number']}]

        with conn.connect() as con:
            con.execute(text(query), final_input)
            con.commit()

    def insert_credit_triggered_by_mudasir_log(self): # when we buy feed
        conn=self.create_connection()
        dff=self.fetch_debit_credit_log()
        feed_rate = feed_class.extract_feed_rate()
        feed_rate=feed_rate[feed_rate['feed_provider']=='Mudasir']
        max_id=dff['car_number'].max()
        # remove this if statement later. replace with:
        #  max_id=int(max_id) # so that it is compatible with mysql
        # max_id=max_id+1
        if 'int' in str(type(max_id)):
            max_id=int(max_id) # so that it is compatible with mysql
            max_id=max_id+1
        else:
            max_id=56
            max_id=int(max_id)
        
        final_input={}
        party_count={}
        input_keys=[]
        final_input['credit_date']=self.inputs['date']
        for i in self.inputs:
            if type(self.inputs[i])==dict:
                final_input['debit_amount'] = 0
                final_input['party'] = 'Siddiq'
                # final_input['week'] = int(pd.to_datetime(self.inputs['date']).strftime("%W"))
                final_input['credit_description'] = f"Paid to mudasir feed car number {max_id}"
                for j in self.inputs[i]['feed_bifurcation'].keys():
                    xx=feed_rate[feed_rate['id']==int(feed_rate[feed_rate['product_name']==j]['id'].max())]
                    ratee = (xx['rate'].iloc[0] - (xx['rate'].iloc[0] * (xx['discount']/100))) + xx['gst_per_bag'].iloc[0]
                    amount_for_feed=ratee.iloc[0]*self.inputs[i]['feed_bifurcation'][j]
                    total_amount=total_amount+amount_for_feed                
                # total_amount=self.feed_rate*self.inputs[i]['bori_amount']
                amount_paid=total_amount - self.inputs[i]['bilti_payment']
                final_input['credit_amount'] = amount_paid
                final_input['car_number'] = max_id
                max_id=max_id+1
                # if final_input['party'] not in party_count:
                #     party_count[final_input['party']] = 0
                # else:
                #     party_count[final_input['party']]=party_count[final_input['party']]+1
                # ids=dff[(dff['date']==self.inputs['date']) & (dff['party']==self.inputs[i]['party'])]['id'].to_list()
                # final_input['report_id'] = ids[party_count[final_input['party']]]
    
                query = "insert into debit_credit_table (credit_date, debit_amount, party, credit_description, credit_amount, car_number) \
                values (:credit_date, :debit_amount, :party,credit_description, :credit_amount, :car_number)"
                with conn.connect() as con:
                    con.execute(text(query), final_input)
                    con.commit()

    def update_credit_triggered_by_mudasir_log(self):
        conn=self.create_connection()
        dff=feed_class.fetch_feed_log()
        df=dff[dff['car_number']==self.inputs['car_number']]
        feed_rate = feed_class.extract_feed_rate()
        feed_rate=feed_rate[feed_rate['feed_provider']=='Mudasir']
        final_input={}
        total_amount=0
        # if 'amount' in self.inputs.keys():
        #     bori_amount = self.inputs['amount']
        # else:
        #     bori_amount=int(df['amount'].iloc[0])
        if 'feed_bifurcation' in self.inputs:
            # st.write(self.inputs['feed_bifurcation'])
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
                
        if 'bilti_payment' in self.inputs.keys():
            bilti_payment = self.inputs['bilti_payment']
        else:
            bilti_payment=float(df['bilti_payment'].iloc[0])
        
        if 'date' in self.inputs.keys():
            final_input['credit_date'] = self.inputs['date']
        # total_amount=self.feed_rate*bori_amount
        amount_paid=total_amount - bilti_payment
        # st.write(amount_paid)
        final_input['credit_amount'] = amount_paid
        final_input['car_number'] = self.inputs['car_number']
        columns_to_update=final_input.keys()
        set_clause = ', '.join(f"{i}=:{i}" for i in columns_to_update if i != 'car_number')
        query = f"update debit_credit_table set {set_clause} where car_number=:car_number"
        # recs=[{'1': self.inputs['arrival_date'], '2': self.inputs['arrival_receipt'], '3': 'ARRIVED', '4': self.inputs['car_number']}]

        with conn.connect() as con:
            con.execute(text(query), final_input)
            con.commit()
            
    @staticmethod
    def fetch_debit_credit_log():
        conn=production_class.create_connection()
        query="select * from debit_credit_table"
        df=pd.read_sql(text(query), conn)
        return df

            


                
