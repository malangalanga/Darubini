import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def cloud():

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
	
	
	
	
	import pandas as pd
	import streamlit as st
	from wordcloud import WordCloud
	import matplotlib.pyplot as plt
	import re

	# Assuming your DataFrame is named 'df'
	# If not, replace 'df' with the actual name of your DataFrame
	df = data_from_mysql
	
	#----------------------------------------------------------------
	#Cleaning tweets data
	# Function to remove URLs from text
	def remove_urls(text):
    		return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                  '', text)

	# Apply the function to the 'text' column
	df['text'] = df['text'].apply(remove_urls)
	
	#Cleaning tweets data
	df['tweet_cleaned']=df['text']
		
	#----------------------------------------------------------------
		
	# Concatenate all text in the 'text' column
	all_text = ' '.join(df['tweet_cleaned'].astype(str))

	# Generate a word cloud
	wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_text)

	# Streamlit app
	st.title('Frequent Hate Speech Words')

	# Display the word cloud using st.image
	#st.image(wordcloud.to_array(), use_column_width=True, format='PNG')

	# Display the word cloud using st.image
	st.image(wordcloud.to_array(), caption=' ', use_column_width=True)


	# Optionally, you can also display the DataFrame or any other information below the word cloud
	#st.write("Data Table:")
	#st.dataframe(df)


   


