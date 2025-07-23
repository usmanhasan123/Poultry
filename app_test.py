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

password=password=quote_plus('Oxygen123$')
# conn=mysql.connector.connect(host='127.0.0.1', port=3307, user='user', password=password, database='poultry_db')
conn = create_engine(f"mysql+mysqlconnector://user:{password}@localhost:3307/poultry_db")
