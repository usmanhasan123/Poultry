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

password=password=quote_plus('lDADsHdkAnShLwwkLmTFTkMqKLeEZXmP')
conn=mysql.connector.connect(host='shortline.proxy.rlwy.net', port=39233, user='root', password=password, database='sql12791552')
# conn = create_engine(f"mysql+mysqlconnector://sql12791552:{password}@sql12.freesqldatabase.com:3306/sql12791552")

if st.button('Show report'):
    query="select * from daily_production"
    df=pd.read_sql(text(query), conn)
    # df=production_class.fetch_daily_report()
    # df2=production_class.fetch_daily_production_table()
    # colss=st.columns(2)
    st.write(df)
    # colss[1].write(df2)
