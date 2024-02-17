import streamlit as st
import os
import importlib




########################################################################

#import streamlit as st
#from session_manager import is_authenticated

#st.title("Other Streamlit App")

# Check if the user is authenticated
#if is_authenticated("username_here"):  # Replace "username_here" with the actual username
    #st.success("Authenticated! You can access this app.")
    # ... (The rest of your app logic)
#else:
#    st.error("Not authenticated! Please log in.")

############################################################################






def load_module(module_path):
    spec = importlib.util.spec_from_file_location("module_name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Set page configuration
st.set_page_config(page_title="Darubini 1.0", page_icon="🌐")

# Create columns for the logo and title
col1, col2 = st.columns([1, 3])

# Add a logo with reduced size in the first column
logo_path = "logoX.svg"
#col1.image(logo_path, caption="Your System Logo", width=150)  # Set a fixed width for the logo
col1.image(logo_path, caption="", width=150)  # Set a fixed width for the logo

# Add the system title on the right of the logo in the second column
col2.title("Darubini 1.0")

# Reduce the separation between the logo and the title using HTML style tag
col1.markdown("<style>h1{margin-left: -70px;}</style>", unsafe_allow_html=True)


# Draw a 1px solid line below all contents of the title, extending to the end of the page
st.markdown(
    """
    <style>
        hr {
            border: 1px solid #4CAF50;  # You can change the color by modifying the hex code
            width: 100%;
            margin-top: 0;
            margin-bottom: 0;
        }
    </style>
    <hr>
    """,
    unsafe_allow_html=True,
)



#****************************************************************************************


import streamlit as st
from importlib import util

def load_and_run_module(file_path):
    spec = util.spec_from_file_location("custom_module", file_path)
    custom_module = util.module_from_spec(spec)
    spec.loader.exec_module(custom_module)

    return custom_module

# Sidebar
st.sidebar.header("Menu")

# Specify the file path here
file_path = "searching4A.py"

# Create a menu to access various functions
menu_options = ["Select Operation", "Run Hate Speech Detection Model", "Display Hate Speech Data", "Hate Speech Distribution Map", "Search the system","Visualizations"]
#choice = st.sidebar.selectbox("Menu", menu_options)
choice = st.sidebar.selectbox("",menu_options)


# Load and display the selected functionality
if choice == "Select Operation":
    st.subheader("Welcome to Darubini: A social media hate speech detector")
    st.write("Darubini is an application for detecting political hate speech that is propagated over social media platforms in Kenya. Darubini is a Swahili word for telescope i.e., an optical instrument for observing distant astronomical objects like stars. Searching for hate-speech over social media platforms is synonymous to searching for new heavenly objects among the many stars in sky")
    
    
# Load and display the selected functionality
elif choice == "Run Hate Speech Detection Model":
    st.subheader("Hate speech detection model running")
    st.write("The model is running. It may take a while to complete depending on the size of the data. Please be patient.......")
    st.write(" ***************** Please read the README file for instructions on running the model ******************")
    #*******************************************************************************************
    
    # Run the loaded module only when "Run classification model" is selected
    
    #file_path4 = "modelA_FIN_Progress.py"
    file_path4 = "README"
    #new_module4 = load_and_run_module(file_path4)

    #if 'run_model' in dir(new_module4) and callable(new_module4.run_model):
    #    new_module4.run_model()
    #else:
    #    st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'run_model'.")
        
    
    #*******************************************************************************************

# Load and display the selected functionality
elif choice == "Hate Speech Distribution Map":
    st.subheader("Hate Speech Distribution Map in Kenya")
    st.write("This is a map showing the distribution of hate speech discourses over X (previously Tweeter) social media in Kenya for the sample dataset we have")
    
    #*******************************************************************************************
    
    # Run the loaded module only when "Hate Speech Distribution Map" is selected
    
    file_path2 = "Hate_Map3.py"
    
    new_module2 = load_and_run_module(file_path2)

    if 'display_map' in dir(new_module2) and callable(new_module2.display_map):
        new_module2.display_map()
    else:
        st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'display_map'.")
        
    
    #*******************************************************************************************

elif choice == "Run classification model":
    st.subheader("classification_model Content")
    st.write("This is the content for classification_model.")
elif choice == "Display Hate Speech Data":
    #st.subheader("Hate Speech Data")
    st.subheader("")

    file_path3 = "report_TestingQ2.py"
    
    # Run the loaded module only when "Search the system" is selected
    new_module3 = load_and_run_module(file_path3)

    #if 'full_data' in dir(new_module3) and callable(new_module3.full_data):
    #    new_module3.full_data()
    #else:
        #st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'full_data'.")
        #st.sidebar.error("")
    
    #*******************************************************************************************

elif choice == "Run classification model":
    st.subheader("classification_model Content")
    st.write("This is the content for classification_model.")
elif choice == "Search the system":
    #st.subheader("Function 3 Content")
    st.subheader("")

    #>>>>>>>>>>>>>>>>>>>>>>>>>
    # Run the loaded module only when "Search the system" is selected
    new_module = load_and_run_module(file_path)

    if 'search' in dir(new_module) and callable(new_module.search):
        new_module.search()
    else:
        st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'search'.")    
    
 #*******************************************************************************************

elif choice == "Visualizations":
    #st.subheader("Function 3 Content")
    st.subheader("Visualizations")
    
    
    # Sidebar
    #st.sidebar.header("Menu2")
    
     
    # Create a menu to access various functions
    menu_options = ["Select visualization","Bar Graphs", "Time series", "Word Cloud"]
    
    #choice = st.sidebar.selectbox("Menu", menu_options)
    choice = st.sidebar.selectbox("",menu_options)

#*************************************************************************************************
	# Load and display the selected functionality
if choice == "Bar Graphs":
	st.subheader("Bar Graphs")
	st.write("The following figures show various bar graphs for the hate-speech dataset.")
	#*******************************************************************************************

	# Run the loaded module only when "Run classification model" is selected
	file_pathA = "Bar_graphs.py"
	
	new_moduleA = load_and_run_module(file_pathA)
	if 'graphs' in dir(new_moduleA) and callable(new_moduleA.graphs):
		new_moduleA.graphs()
	else:
		st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'graphs'.")
        
    
   
#*************************************************************************************************
	# Load and display the selected functionality
elif choice == "Time series":
	st.subheader("Time series")
	st.write("The following figures show a time series for the hate-speech dataset.")
	#*******************************************************************************************

	# Run the loaded module only when "Run classification model" is selected
	file_pathB = "time_series_plot.py"
	
	new_moduleB = load_and_run_module(file_pathB)
	if 'time_series' in dir(new_moduleB) and callable(new_moduleB.time_series):
		new_moduleB.time_series()
	else:
		st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'time_series'.")
        
    
    #*******************************************************************************************    
       
	# Load and display the selected functionality
elif choice == "Word Cloud":
	st.subheader(" ")
	st.write("The following figure shows most frequent hate-speech words.")
	#*******************************************************************************************

	# Run the loaded module only when "Run classification model" is selected
	file_pathC = "Word_cloud.py"
	
	new_moduleC = load_and_run_module(file_pathC)
	if 'cloud' in dir(new_moduleC) and callable(new_moduleC.cloud):
		new_moduleC.cloud()
	else:
		st.sidebar.error("Invalid .py file or function. Make sure it contains a callable function named 'cloud'.")
        
    
    #*******************************************************************************************    
                   
# Footer
footer = """
    <hr style="margin-top: 1em; margin-bottom: 1em;">
    <p style="text-align: center; font-size: 0.8em; color: #888;">Developed by: Dr. Malanga Kennedy Ndenga & Dr. Victor Mokaya Mageto - Kirinyaga University</p>
    """
st.markdown(footer, unsafe_allow_html=True)        
        



