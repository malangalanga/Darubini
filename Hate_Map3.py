import streamlit as st
import pandas as pd
import json
import folium
import pymysql
from sqlalchemy import create_engine
from streamlit_folium import folium_static



def display_map():

    
        #st.title("Hate Speech Locations Map")
        st.title("")
    
    
        ##########################################################################################################
        #Reading the dataset from a mysql database
        ##########################################################################################################
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
        #database = 'Darubini'
    
        #--- MySQL query to select data from a table
        #query = 'SELECT * FROM Hate_speech_table'
    
        #--- Create a MySQL connection
        #mysql_connection = create_mysql_connection(host, user, password, database)
    
        #--- Read data from MySQL and display as DataFrame
        #data_from_mysql = read_data_from_mysql(mysql_connection, query)
        
        
        #--- Reading classified data directly from a csv file
        data_from_mysql = pd.read_csv('https://github.com/malangalanga/Darubini/blob/master/Final_Hate_df')
    
                
        #--- Creating a dataframe compatible with the maps app
        geo_df = data_from_mysql
    
        ########################################################################################################
    
        #Stripping geo column for the name of the location
        #########################################################################################################
    
        #Removing all strings before and including "["
        #geo_df['geo'].str.split('"name":"').str[-1].str.strip()
    
        #Rejoining media series to the main DataFrame after removing all strings before and including "id":"
        geo_df['Hate_Speech_location_Name']=geo_df['geo'].str.split('"name":"').str[-1].str.strip()
    
        #Removing all strings after and including "]"
        #geo_df['Hate_Speech_location_Name'].str.split('","id":"').str[0]
    
        #Rejoining media series to the main DataFrame after removing all strings after and including ",""
        geo_df['Hate_Speech_location_Name']=geo_df['Hate_Speech_location_Name'].str.split('","id":"').str[0]
    
        #Removing all strings after and including "]"
        #geo_df['Hate_Speech_location_Name'].str.split('"}').str[0]
    
        #Rejoining media series to the main DataFrame after removing all strings after and including ",""
        geo_df['Hate_Speech_location_Name']=geo_df['Hate_Speech_location_Name'].str.split('"}').str[0]
    
        #Removing all strings after and including "]"
        #geo_df['Hate_Speech_location_Name'].str.split('","country_code":').str[0]
    
        #Rejoining media series to the main DataFrame after removing all strings after and including ",""
        geo_df['Hate_Speech_location_Name']=geo_df['Hate_Speech_location_Name'].str.split('","country_code":').str[0]
    
        #Removing all strings after and including "]"
        #geo_df['Hate_Speech_location_Name'].str.split('","geo":{').str[0]
    
        #Rejoining media series to the main DataFrame after removing all strings after and including ",""
        geo_df['Hate_Speech_location_Name']=geo_df['Hate_Speech_location_Name'].str.split('","geo":{').str[0]
    
        #################################
    
        #Stripping geo column for the bbox coordinates
        ############################################################################################################
    
        #Removing all strings before and including "["
        #geo_df['geo'].str.split('bbox":').str[-1].str.strip()
    
        #Rejoining media series to the main DataFrame after removing all strings before and including "id":"
        geo_df['bbox']=geo_df['geo'].str.split('bbox":').str[-1].str.strip()
    
        #Removing all strings after and including "]"
        #geo_df['bbox'].str.split(',"properties').str[0]
    
        #Rejoining media series to the main DataFrame after removing all strings after and including ",""
        geo_df['bbox']=geo_df['bbox'].str.split(',"properties').str[0]
    
        ############################################################################################################
    
        #Dropping empty records
        geo_df2 = geo_df[['bbox','Hate_Speech_location_Name']].dropna()
    
        ############################################################################################################
    
        #Creating 'min_lat', 'min_lon', 'max_lat', 'max_lon' cloumns from the bbox data
        ###########################################################################################################
    
        # Assuming geo_df2 is your DataFrame and 'bbox' is the column with coordinates
        geo_df2['bbox'] = geo_df2['bbox'].apply(json.loads)
    
        # Create separate columns for each coordinate
        geo_df2[['min_lat', 'min_lon', 'max_lat', 'max_lon']] = pd.DataFrame(geo_df2['bbox'].tolist(), index=geo_df2.index)
    
        # Drop the original 'bbox' column if needed
        geo_df2 = geo_df2.drop('bbox', axis=1)
    
        geo_dfX = geo_df2.dropna()
                   
        ##########################################################################################################
    
        #Calculating Latitude and Longitudes from bbox coordinates
        ############################################################################################################
        def calculate_center(bbox):
            min_lat, min_lon, max_lat, max_lon = bbox
            center_lat = (min_lat + max_lat) / 2
            center_lon = (min_lon + max_lon) / 2
            return center_lat, center_lon
    
        # Calculate the center of each bounding box
        geo_dfX['Latitude'], geo_dfX['Longitude'] = zip(*geo_dfX[['min_lat', 'min_lon', 'max_lat', 'max_lon']].apply(calculate_center, axis=1))
        ###########################################################################################################
        #Adding more information on the geo_dfX dataframe
    
        geo_dfX['text']=geo_df['text']
    
        geo_dfX['Anonymized_author_id']=geo_df['Anonymized_author_id']
        #geo_dfX
    
        ###########################################################################################################
    
        #Plotting the points on a map
        ###########################################################################################################
    
        # Create a map centered at the mean of all points
        map_center = [geo_dfX['Longitude'].mean(), geo_dfX['Latitude'].mean()]

        map_object = folium.Map(location=map_center, zoom_start=12)

        # Plot all points on the map with pop-up windows
        for index, row in geo_dfX.iterrows():
            folium.Marker(
                location=[row['Longitude'], row['Latitude']],
                popup=f"""
                    <strong>Location Name:</strong> {row['Hate_Speech_location_Name']}<br><br>
                    <strong>Latitude:</strong> {row['Latitude']}<br>
                    <strong>Longitude:</strong> {row['Longitude']}<br><br>
                    <strong>Hate Text:</strong> {row['text']}<br><br>
                    <strong>Author ID:</strong> {row['Anonymized_author_id']}
                """,
                icon=folium.Icon(color='red')
            ).add_to(map_object)

        # Display the map using Streamlit
    
    
    
        folium_static(map_object)




	
	

