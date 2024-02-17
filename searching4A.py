import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

from datasets import load_dataset,DatasetDict
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import tempfile
import pymysql
from sqlalchemy import create_engine
import time


def search():
    #############################################
    #Read data from MySQL into a DataFrame      #
    #############################################

    #--- Function to establish a MySQL connection
    #def create_mysql_connection(host, user, password, database):
    #    return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

    #--- Function to read data from MySQL database into a DataFrame
    #def read_data_from_mysql(connection, query):
    #    return pd.read_sql(query, connection)

    #--- MySQL database connection details
    #host = 'localhost'
    #user = 'root'
    #password = 'mysql'
    #database = 'Darubini3'

    #--- MySQL query to select data from a table
    #query = 'SELECT * FROM Hate_speech_table'

    #--- Create a MySQL connection
    #mysql_connection = create_mysql_connection(host, user, password, database)

    #--- Read data from MySQL and display as DataFrame
    #data_from_mysql = read_data_from_mysql(mysql_connection, query)
    
    
    #--- Reading classified data directly from a csv file
    data_from_mysql = pd.read_csv('https://github.com/malangalanga/Darubini/blob/master/Final_Hate_df')
    

    #--- Streamlit app
    st.title("Filter Hate Speech Records")

    #--- Iterate through columns and create text input for each
    for column in data_from_mysql.columns:
        filter_value = st.text_input(f" {column}", "")
        if filter_value:
            data_from_mysql = data_from_mysql[data_from_mysql[column].astype(str).str.contains(filter_value, case=False)]

    #--- Display the filtered DataFrame
    st.dataframe(data_from_mysql)



