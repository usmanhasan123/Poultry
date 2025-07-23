import os
os.chdir('./')
import streamlit as st
import datetime
from get_and_upload_daily_production import production_class

password=password=quote_plus('Oxygen123$')
# conn=mysql.connector.connect(host='127.0.0.1', port=3307, user='user', password=password, database='poultry_db')
conn = create_engine(f"mysql+mysqlconnector://user:{password}@localhost:3307/poultry_db")
