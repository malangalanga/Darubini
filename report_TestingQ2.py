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
from reportlab.pdfgen import canvas
import base64



#def full_data():
    #############################################
    #Read data from MySQL into a DataFrame      #
    #############################################

    # Function to establish a MySQL connection
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
data_from_mysql = pd.read_csv('Final_Hate_df')
    

df = data_from_mysql.drop(columns=['Unnamed: 0'])

#df = data_from_mysql

df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

# Function to generate PDF report for a single record
def generate_pdf_report(record):
    filename = f"{record['Anonymized_author_NAME']}_report.pdf"
    c = canvas.Canvas(filename)

    # Add content to the PDF
    c.drawString(100, 750, f"Name: {record['Anonymized_author_NAME']}")
    c.drawString(100, 760, f"Social Media identity: {record['Anonymized_author_id']}")
    c.drawString(100, 770, f"Social Media User Name: {record['Anonymized_author_USERNAME']}")
    c.drawString(100, 780, f"Hate Speech post ID: {record['Anonymized_tweet_id']}")
    c.drawString(100, 790, f"Hate Speech post text: {record['text']}")
    c.drawString(100, 800, f"Time of posting the message: {record['created_at']}")
    c.drawString(100, 710, f"Location of posting the message: {record['Hate_Speech_location_Name']}")

    # Save the PDF
    c.save()

    return filename

# Streamlit app
st.title('Hate Speech Data: Filter and Generate Reports')

# Display the dataframe before filtering
st.dataframe(df)
#--------------------------------------------------------------------------------------------
#Pagination code to be put here


#--------------------------------------------------------------------------------------------

# Set default minimum created_at to January 1, 2016
default_min_created_at = pd.to_datetime('2016-01-01', utc=True)

# Filter the dataframe based on user criteria
filter_name = st.text_input('Enter Hate speech author NAME:')
filter_username = st.text_input('Enter Hate speech author social media USERNAME:')
filter_author_id = st.text_input('Enter Hate speech author social media ID:')
filter_created_at_min = st.date_input('Enter minimum created_at:', value=default_min_created_at)
filter_created_at_max = st.date_input('Enter maximum created_at:')
filter_tweetID = st.text_input('Enter Hate Speech post ID:')
filter_Hate_Speech_location_Name = st.text_input('Enter location of posting criteria:')

# Convert date inputs to datetime64[ns, UTC] only if they are not empty
filter_created_at_min = pd.to_datetime(filter_created_at_min, utc=True, errors='coerce') if filter_created_at_min else pd.NaT
filter_created_at_max = pd.to_datetime(filter_created_at_max, utc=True, errors='coerce') if filter_created_at_max else pd.NaT

# Apply filters dynamically
filter_conditions = (
    (df['Anonymized_author_NAME'].str.contains(filter_name, case=False) if filter_name else True) &
    (df['Anonymized_author_USERNAME'].str.contains(filter_username, case=False) if filter_username else True) &
    (df['Anonymized_author_id'].str.contains(filter_author_id, case=False) if filter_author_id else True) &
    ((df['created_at'] >= filter_created_at_min) if not pd.isna(filter_created_at_min) else True) &
    ((df['created_at'] <= filter_created_at_max) if not pd.isna(filter_created_at_max) else True) &
    (df['id'].str.contains(filter_tweetID, case=False) if filter_tweetID else True) &
    (df['Hate_Speech_location_Name'].str.contains(filter_Hate_Speech_location_Name , case=False) if filter_Hate_Speech_location_Name  else True)
)

filtered_df = df[filter_conditions]

# Display the filtered dataframe
st.dataframe(filtered_df)

#####################################################################################

import streamlit as st
import pandas as pd
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import weasyprint
import cairosvg
import textwrap
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Assume that `filtered_df` is your DataFrame containing the records


def wrap_text(pdf, text, x, y, row_height, max_width):
    lines = textwrap.wrap(text, width=50)  # Adjust the width as needed
    for line in lines:
        pdf.drawString(x + 170, y, line)
        y -= row_height


# Create a function to generate a professional PDF report
def generate_pdf_report(record):
    buffer = BytesIO()

    # Create a canvas for PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
   #------------------------------------------------ 
    # Set a custom font that supports emojis (replace with the path to your font file)
    #font_path = "/home/malanga/Environments/noto-emoji-2.042(2)/noto-emoji-2.042/fonts/NotoColorEmoji.ttf"
       
    # Embed the NotoColorEmoji font directly in the PDF
    #pdfmetrics.registerFont(TTFont('NotoColorEmoji', font_path))
    #pdf.setFont('NotoColorEmoji', 12)

    #------------------------------------------------
    
    # Add organization logo, motto, and address
    #pdf.drawInlineImage('/home/malanga/Environments/logo.png', 20, 695, width=75, height=75)https://github.com/malangalanga/Darubini/blob/master/logo.png
    pdf.drawInlineImage('https://github.com/malangalanga/Darubini/blob/master/logo.png', 20, 695, width=75, height=75)
    pdf.setFont("Times-Bold", 36)
    pdf.drawString(100, 735, "Darubini")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(100, 712, "P.O. Box 44405 - 00100 Nairobi.")
    pdf.drawString(100, 698, "Email: darubini@kyu.ac.ke")
    
    # Set the line width and dash pattern
    pdf.setLineWidth(2.5)  # Adjust the thickness as needed
    
    pdf.line(100, 690, 570, 690) 
    pdf.setDash(1, 0)  # No dash pattern (solid line)

    # Set a custom font that supports emojis
    #pdf.setFont("DejaVuSans", 12)

    #pdf.setFont("Times-Roman", 12)

    # Add record details in a table
    pdf.setFont("Times-Bold", 14)
    pdf.drawString(190, 630, f"Hate Speech Report for {record['Anonymized_author_NAME']}")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(190, 629, "_______________________________________")

      
    data = [
        ("Name", str(record['Anonymized_author_NAME'])), 
        ("Social Media Identity", str(record['Anonymized_author_id'])),
        ("Social Media User Name", str(record['Anonymized_author_USERNAME'])),
        ("Hate Speech Post ID", str(record['Anonymized_tweet_id'])),
        ("Hate Speech Posting Location", str(record['Hate_Speech_location_Name'])),
        ("Time of Posting", str(record['created_at'])),
        ("Hate Speech Post Text", str(record['text'])),
        # Add more fields as needed
    ]
    
    
    
          
    # Add record details in a table
    pdf.setFont("Times-Roman", 12)
    row_height = 20
    x, y = 120, 600
    
    for label, value in data:
        pdf.drawString(x, y, label)
        pdf.drawString(x + 150, y, ":")
        
        
        # Increase the x-axis space for writing text before wrapping
        x_text = x + 200
        
        # Get the initial y-coordinate for the value
        initial_y = y
        
               
        # Manually handle line wrapping for the value
        #wrap_text(pdf, value, max_width=300)  # Adjust the width as needed
        wrap_text(pdf, str(value), x + 0, y, row_height, max_width=800)
        y -= row_height  # Adjust the y-coordinate for the next label  

        # Adjust the y-coordinate for the next label
        y = initial_y - row_height
    
        
    #row_height = 24
    #x, y = 100, 600    
    #for label, value in data:
        #pdf.setFont("Times-Bold", 12)
    #    pdf.drawString(x, y, label)
    #    pdf.drawString(x + 150, y, ":")
    #    pdf.drawString(x + 170, y, value)
    #    y -= row_height
    
      

    #pdf.drawString(100, 405, "_____________________________________________________________________________")
    
    pdf.setFont("Times-Bold", 13)
    pdf.drawString(160, 180, f"NOTE: This output has been anonymized for security reasons")


    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.setFont("Times-Italic", 10)
    pdf.drawString(220, 50, f"Printed on: {timestamp}")

    pdf.save()

    buffer.seek(0)
    return buffer

# Streamlit app code
if st.button('Generate PDF Reports'):
    for index, record in filtered_df.iterrows():
        pdf_buffer = generate_pdf_report(record)
        base64_pdf = base64.b64encode(pdf_buffer.read()).decode()
        download_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{record["Anonymized_author_NAME"]}_report.pdf">Download PDF Report for {record["Anonymized_author_NAME"]}</a>'
        st.markdown(download_link, unsafe_allow_html=True)




