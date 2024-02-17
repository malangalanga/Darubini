
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import streamlit as st



def graphs():

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


	#################################################
	#Hate Speech Occurrences per Year               #
	#################################################

	# Set the dark background style
	sns.set(style="darkgrid")
	
	df = data_from_mysql

	# Convert 'created_at' column to datetime format
	df['created_at'] = pd.to_datetime(df['created_at'])

	# Extract the year and month from the 'created_at' column
	df['year'] = df['created_at'].dt.year
	df['month'] = df['created_at'].dt.month

	# Group by year and month, then count the occurrences of hate speech
	df_grouped = df[df['Detections'] == 'Hate Speech'].groupby(['year', 'month']).size().reset_index(name='count')

	# Map month numbers to month names
	df_grouped['month'] = df_grouped['month'].apply(lambda x: calendar.month_abbr[x])

	# Streamlit App
	st.title('Hate Speech Bar Graphs')

	# Sidebar to filter data if needed
	st.sidebar.header('Filter Data')
	# Add filter options if needed, e.g., st.sidebar.checkbox, st.sidebar.selectbox

	# Plot the bar graph using Seaborn
	fig, ax = plt.subplots(figsize=(12, 6))
	sns.barplot(x='month', y='count', hue='year', data=df_grouped, palette='viridis', ax=ax)
	plt.title('Hate Speech Occurrences per Month for Each Year')
	plt.xlabel('Month')
	plt.ylabel('Number of Occurrences')
	plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')

	# Display the plot in Streamlit
	st.pyplot(fig)
	
	
	#################################################
	#Hate Speech Occurrences per Year               #
	#################################################

	df2 = data_from_mysql

	# Convert 'created_at' column to datetime format
	df2['created_at'] = pd.to_datetime(df2['created_at'])

	# Extract the year from the 'created_at' column
	df2['year'] = df['created_at'].dt.year

	# Group by year and count the occurrences of hate speech
	df_grouped2 = df2[df2['Detections'] == 'Hate Speech'].groupby('year').size().reset_index(name='count')

	fig2, ax2 = plt.subplots(figsize=(10, 6))
	sns.barplot(x='year', y='count', data=df_grouped2, palette='viridis')
	plt.title('Hate Speech Occurrences per Year')
	plt.xlabel('Year')
	plt.ylabel('Number of Occurrences')

	# Display the plot in Streamlit
	st.pyplot(fig2)


	###################################################################
	#                                                                 #
	#Hate Speech Occurrences per Month for the entire period          #
	###################################################################


	df3 = data_from_mysql

	# Convert 'created_at' column to datetime format
	df3['created_at'] = pd.to_datetime(df3['created_at'])

	# Extract the year from the 'created_at' column
	df3['month'] = df3['created_at'].dt.month

	# Group by year and count the occurrences of hate speech
	df_grouped3 = df3[df3['Detections'] == 'Hate Speech'].groupby('month').size().reset_index(name='count')

	# Map month numbers to month names
	df_grouped3['month'] = df_grouped3['month'].apply(lambda x: calendar.month_abbr[x])

	# Plot the bar graph using Seaborn
	fig3, ax3 = plt.subplots(figsize=(10, 6))
	sns.barplot(x='month', y='count', data=df_grouped3, palette='viridis')
	plt.title('Hate Speech Occurrences per Month for the entire period')
	plt.xlabel('Month')
	plt.ylabel('Number of Occurrences')

	# Display the plot in Streamlit
	st.pyplot(fig3)

