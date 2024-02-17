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


########################################################################################################
# Create a progress bar
#progress_bar = st.progress(0)

# Create a text element to display the status
#status_text = st.empty()

########################################################################################################


#progress_bar = st.progress(0)
#Raw_df = pd.read_csv('/home/malanga/Environments/FINAL DATASETS/NEW_Politico104.csv')

Raw_df = pd.read_csv('https://github.com/malangalanga/Darubini/blob/master/Anonymized_Kenyan_political_dataset')

#Sample 10% of the dataframe
#Raw_df=Raw_df.sample(frac =.02)

def run_model():

	import streamlit as st
	
	progress_bar = st.progress(0)
	
	tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

	#model=tf.saved_model.load("/home/malanga/modeled 1st Dec 2023/13")
	model=tf.saved_model.load("https://github.com/malangalanga/Darubini/blob/master/SavedModel19")

	tmpdir = tempfile.mkdtemp()


	##############################################################################################################

	#Reading raw tweets data from a .csv file
	
	#Raw_df = pd.read_csv('/home/malanga/Environments/FINAL DATASETS/NEW_Politico104.csv')

	test_df = Raw_df[Raw_df['text'].notna()]

	#test_df=test_df.sample(frac=0.05)
	
	#progress_bar.progress(1)


	##############################################################################################################


	#Cleaning tweets data

	test_df['tweet_cleaned']=test_df['text'].str.replace('@[A-Za-z0-9]+\s?','',regex=True)

	test_df=test_df[['Anonymized_tweet_id','tweet_cleaned']]

	###############################################################################################################

	#Converting 'tweet_cleaned' data into a list for feeding the model
	test_df.reset_index(inplace=True, drop=True)
	for index, row in test_df.iterrows():
		text = tf.expand_dims(row["tweet_cleaned"], axis=0)
		text = test_df['tweet_cleaned'].values.tolist()

	#progress_bar.progress(2)
	##############################################################################################################

	#Splitting text into chunks

	from more_itertools import chunked
	#text_chunks=list(chunked(text, 100))
	text_chunks=list(chunked(text, 1))

	progress_bar.progress(5)
	#############################################################################################################

	#Renaming the model -- before saving
	loaded = model

	#############################################################################################################
	from tqdm import tqdm  # Import tqdm for the progress bar

	#Analyzing data for detections

	detections = []  # List to store the detected classes

	predict_score_and_class_dict = {0: 'Hate Speech', 1: 'Offensive', 2: 'Neither'}


	# Get the total number of chunks for the progress bar
	total_chunks = len(text)
	
	#progress_bar.progress(15)

	

	
	
	# Use tqdm for the loop and update the Streamlit progress bar
	for i, text_chunk in enumerate(text): #(tqdm(text, desc="Processing chunks", unit="chunk", dynamic_ncols=True, leave=False)):
		try:
			preds = loaded(tokenizer(text_chunk, return_tensors="tf", padding=True, truncation=True))['logits']
			class_preds = np.argmax(preds, axis=1)
			for pred in class_preds:
				detections.append(predict_score_and_class_dict[pred])
		except Exception as e:
			# Handle the exception (you can customize this part based on your needs)
			print(f"Error processing chunk: {text}. Error: {e}")

		# Update the Streamlit progress bar
		progress_bar.progress((i + 1) / total_chunks)
	
	#progress_bar.progress(95)
	 
	#Update the DataFrame column
	test_df['Detections'] = detections

	#############################################################################################################

	#Selecting records detected as hatespeech

	x=test_df.loc[test_df['Detections'] == 'Hate Speech']

	#############################################################################################################

	#Merging Hate_df to the original dataframe i.e test_df and maintaning relevant columns

	Final_Hate_df = Raw_df.merge(x, how='inner', left_on='Anonymized_tweet_id', right_on='Anonymized_tweet_id')

	Final_Hate_df = Final_Hate_df[['Anonymized_tweet_id', 'text', 'created_at', 'Anonymized_author_id', 'lang', 'author', 'entities','referenced_tweets', 'media', 'geo', 'Detections']]


	############################################################################################################

	#Stripping author column for the ID of the person who authored the HATESPEECH
	############################################################################################################

	#Removing all strings before and including ""id":":" 
	#Final_Hate_df['author'].str.split('"id":"').str[-1].str.strip()

	#Rejoining media series to the main DataFrame after removing all strings before and including "id":" 
	#Final_Hate_df['Hate_Speech_authorID']=Final_Hate_df['author'].str.split('"id":"').str[-1].str.strip()

	#Removing all strings after and including ",":......." 
	#Final_Hate_df['Hate_Speech_authorID'].str.split('","').str[0]

	#Rejoining media series to the main DataFrame after removing all strings after and including ",""
	#Final_Hate_df['Hate_Speech_authorID']=Final_Hate_df['Hate_Speech_authorID'].str.split('","').str[0]  

	############################################################################################################
	
	#Stripping author column for the NAME of the person who authored the HateSpeech
	############################################################################################################

	#Removing all strings before and including ""id":":" 
	#Final_Hate_df['author'].str.split('","name":"').str[-1].str.strip()

	#Rejoining media series to the main DataFrame after removing all strings before and including "id":" 
	Final_Hate_df['Hate_Speech_author_NAME']=Final_Hate_df['author'].str.split('","name":"').str[-1].str.strip()

	#Removing all strings after and including ",":......." 
	#Final_Hate_df['Hate_Speech_author_NAME'].str.split('"').str[0]

	#Rejoining media series to the main DataFrame after removing all strings after and including ",":" 
	Final_Hate_df['Hate_Speech_author_NAME']=Final_Hate_df['Hate_Speech_author_NAME'].str.split('"').str[0]  

	############################################################################################################

	#Stripping author column for the USERNAME of the person who authored the HateSpeech
	############################################################################################################

	#Removing all strings before and including ""id":":" (3 marks)
	#Final_Hate_df['author'].str.split('","username":"').str[-1].str.strip()

	#Rejoining media series to the main DataFrame after removing all strings before and including "id":" 
	Final_Hate_df['Hate_Speech_author_USERNAME']=Final_Hate_df['author'].str.split('","username":"').str[-1].str.strip()

	#Removing all strings after and including ",":......." (3 marks)
	#Final_Hate_df['Hate_Speech_author_USERNAME'].str.split('"}').str[0]

	#Rejoining media series to the main DataFrame after removing all strings after and including ",":" (3 maks)
	Final_Hate_df['Hate_Speech_author_USERNAME']=Final_Hate_df['Hate_Speech_author_USERNAME'].str.split('"}').str[0]


	############################################################################################################

	#******************Stripping geo column for the name of the location**********************  
	############################################################################################################

	#Rejoining media series to the main DataFrame after removing all strings before and including "id":" 
	Final_Hate_df['Hate_Speech_location_Name']=Final_Hate_df['geo'].str.split('"name":"').str[-1].str.strip()

	#Rejoining media series to the main DataFrame after removing all strings after and including ",""
	Final_Hate_df['Hate_Speech_location_Name']=Final_Hate_df['Hate_Speech_location_Name'].str.split('","id":"').str[0]

	#Rejoining media series to the main DataFrame after removing all strings after and including ",""
	Final_Hate_df['Hate_Speech_location_Name']=Final_Hate_df['Hate_Speech_location_Name'].str.split('"}').str[0]

	#Rejoining media series to the main DataFrame after removing all strings after and including ",""
	Final_Hate_df['Hate_Speech_location_Name']=Final_Hate_df['Hate_Speech_location_Name'].str.split('","country_code":').str[0]

	#Rejoining media series to the main DataFrame after removing all strings after and including ",""
	Final_Hate_df['Hate_Speech_location_Name']=Final_Hate_df['Hate_Speech_location_Name'].str.split('","geo":{').str[0]


	#***************************************************
	#df = Final_Hate_df
	
	
	#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
	
	Final_Hate_df = Final_Hate_df[['Anonymized_tweet_id', 'text', 'Detections', 'created_at', 'Hate_Speech_author_NAME', 'Hate_Speech_author_USERNAME', 'Anonymized_author_id', 'lang', 'entities', 'referenced_tweets', 'media', 'geo','Hate_Speech_location_Name']] #Add location field!!!!!!!!!!!!
	
	#-----------------------ANONYMIZING SENSITIVE FIELDS---------------------------------------
	# Anonymizer Packages
	
	# Anonymize DF
	from anonymizedf.anonymizedf import anonymize
	# Scrambler
	from random import shuffle
	# Faker
	from faker import Faker
	faker = Faker()
	#faker = Faker("en_GB")
	
	import warnings
	warnings.filterwarnings("ignore")
	
	#-----------------------------------------------------------------------------------------
	anon = anonymize(Final_Hate_df)
	
	# AnonymizeDF can generate fake names
	anon.fake_names("Hate_Speech_author_NAME")
	
	anon.fake_names("Hate_Speech_author_USERNAME")
	
	# dropping unwanted columns
	Final_Hate_df = Final_Hate_df.drop(columns=['Hate_Speech_author_NAME'])
	Final_Hate_df = Final_Hate_df.drop(columns=['Hate_Speech_author_USERNAME'])
	
	#Renaming new anonymized columns
	Final_Hate_df.rename(columns={'Fake_Hate_Speech_author_NAME':'Anonymized_author_NAME','Fake_Hate_Speech_author_USERNAME':'Anonymized_author_USERNAME' }, inplace=True)
	
	#------------------------------------------------------------------------------------------

		
	#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
	
	#Writing final hate dataframe to a location
	Final_Hate_df.to_csv("https://github.com/malangalanga/Darubini/blob/master/Final_Hate_df")




	#---- For production, it is safer to store the data in a database like mysql using the following code --------------
	#import streamlit as st
	#import pandas as pd
	#from sqlalchemy import create_engine

	#---- Function to establish a MySQL connection
	#def create_mysql_connection(host, user, password, database):
    	#	return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

	#---- Function to read data from a CSV file
	#def read_csv(file_path):
	#	return pd.read_csv(file_path)

	#---- Function to stream data into MySQL database
	#def stream_data_to_mysql(connection, data, table_name):
    	#	data.to_sql(table_name, connection, if_exists='append', index=False)
	
	
	
	#st.title(' ')
	
	#---- MySQL database connection details
	#host = 'localhost'
	#user = 'root'
	#password = 'mysql'
	#database = 'Darubini'
	
	#---- MySQL table name
	#table_name = 'Hate_speech_table'
	
	#---- Display data in Streamlit
	#st.subheader('Hate Speech Data')
	#st.dataframe(Final_Hate_df)
	
	#---- Create a MySQL connection
	#mysql_connection = create_mysql_connection(host, user, password, database)
	
	
	#---- Stream data into MySQL database
	
	#st.subheader('')
	#with st.spinner('Streaming data to MySQL...'):
	#	stream_data_to_mysql(mysql_connection, Final_Hate_df, table_name)
		
	st.success("Data Streaming to the database completed.")
	
	
	
	
	
	
	
	
	
	
	
