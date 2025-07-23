import os
os.chdir('./')
import streamlit as st
import datetime
from get_and_upload_daily_production import production_class

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pyodbc
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

password=password=quote_plus('dzgmxiL4e7')
# conn=mysql.connector.connect(host='sql12.freesqldatabase.com', port=3306, user='sql12791552', password=password, database='sql12791552')
conn = create_engine(f"mysql+mysqlconnector://user:{password}@localhost:3307/poultry_db")

if st.button('Show report'):
    df=production_class.fetch_daily_report()
    # df2=production_class.fetch_daily_production_table()
    # colss=st.columns(2)
    st.write(df)
    # colss[1].write(df2)
