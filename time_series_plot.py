import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def time_series():

	#############################################
	#Read data from MySQL into a DataFrame      #
	#############################################


	import pandas as pd
	import pymysql
	from sqlalchemy import create_engine

	#--- Function to establish a MySQL connection
	#def create_mysql_connection(host, user, password, database):
	#	return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

	#--- Function to read data from MySQL database into a DataFrame
	#def read_data_from_mysql(connection, query):
	#	return pd.read_sql(query, connection)

	#--- MySQL database connection details
	#host = 'localhost'
	#user = 'root'
	#password = 'mysql'
	#database = 'Darubini'

	#--- MySQL query to select data from a table
	#query = 'SELECT * FROM Hate_speech_table'

	#--- Create a MySQL connection
	#mysql_connection = create_mysql_connection(host, user, password, database)

	#--- Read data from MySQL and display as DataFrame
	#data_from_mysql = read_data_from_mysql(mysql_connection, query)
	
	
	#--- Reading classified data directly from a csv file
	data_from_mysql = pd.read_csv('https://github.com/malangalanga/Darubini/blob/master/Final_Hate_df')
    


	
	################################################################################
	#
	#Time Series plot
	################################################################################
	
	
	df = data_from_mysql

	import pandas as pd
	import plotly.express as px
	import streamlit as st

	# Assuming your data frame is named df
	# Convert 'created_at' to datetime format if it's not already
	df['created_at'] = pd.to_datetime(df['created_at'])

	# Filter the data for the desired time range (2017 to 2022)
	mask = (df['created_at'] >= '2017-01-01') & (df['created_at'] <= '2022-12-31')

	# Check if there are valid rows after filtering
	if df.loc[mask].empty:
		st.warning("No data available for the selected time range.")
	else:
		df_filtered = df.loc[mask]

		# Group by date and count the occurrences of 'Hate Speech'
		time_series_data = df_filtered.groupby(df_filtered['created_at'].dt.to_period("M")).size().reset_index(name='count')

		# Convert 'created_at' to datetime format in time_series_data
		time_series_data['created_at'] = time_series_data['created_at'].dt.to_timestamp()

		# Streamlit app
		st.title('Hate Speech Detections Time Series (2017-2022)')

		# Interactive time series plot using Plotly Express
		fig = px.line(time_series_data, x='created_at', y='count', markers=True, labels={'count': 'Number of Detections'})
		fig.update_layout(title='Time Series Plot of Hate Speech Detections (2017-2022)', xaxis_title='Time', 
								yaxis_title='Number of Detected hate speeches', 
								hovermode='x unified')
		st.plotly_chart(fig)

   


