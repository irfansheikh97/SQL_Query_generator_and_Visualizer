from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from model_methods import get_response, plot_data, read_sql_query, check_api_key

# For local use: Create .env file in project repo and store api key in GOOGLE_API_KEY variable to access locally */
# Load environment variables
# load_dotenv()

# Google API Configuration
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database Path Configuration
# database_path = 'netflix_data.db'

# Streamlit web interface configuration
st.set_page_config(page_title="SQL Query Generator and Visualization Web App", layout="wide", page_icon='📊')

st.markdown("""
     <h1 style="color: DarkOrange; text-align: center; width: 100%;">
     📊 DataQuery Pro: Retrieve Data with Ease
     </h1>
     """, unsafe_allow_html=True)

# streamlit session state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'sql_query' not in st.session_state:
    st.session_state.sql_query = ''

if 'user_db' not in st.session_state:
    st.session_state.user_db = None


def click_button():
    st.session_state.clicked = True


# /*---- New code start ----*/
# Using "with" notation
with st.sidebar:
    st.write('<h4 style="color: #ff3333;">Enter your Gemini API key</h4>',
             unsafe_allow_html=True)
    st.session_state.api_key = st.text_input('Enter API Key', type='password', key='st.session_state.api_key',
                                             label_visibility="collapsed")
    if st.session_state.api_key != '':
        check_api_key(st.session_state.api_key)
        st.session_state.user_db = st.file_uploader("Upload your database file ", type=[".sqlite", '.db', '.sql'])
    genai.configure(api_key=st.session_state.api_key)

if st.session_state.user_db is not None:
    with st.container():
        # Prompt for the Generative Model
        prompt = st.text_area(":red[Enter a Prompt for Model: ]", help="Enter the prompt for AI model to interact with"
                                                                       "your database file. Basically a role of SQL "
                                                                       "Expert/Developer.")
        st.subheader(":rainbow[QUERY PLAYGROUND]", anchor=False)
        col1, col2 = st.columns([6, 1], gap="small", vertical_alignment="bottom")
        with col1:
            # st.write('<h4 style="color: black;">Input your question here:</h4>',unsafe_allow_html=True)
            question = st.text_input("Input your question here: ", key="input", placeholder="Type here...")
        with col2:
            submit = st.button("Get Data", help="Click to submit your question.", on_click=click_button)

    if submit:
        if question and prompt:
            st.session_state.sql_query = get_response(question, prompt)
            try:
                if st.session_state.sql_query:
                    # Write the uploaded file to a temporary location
                    with open('temp_db.sqlite', 'wb') as f:
                        f.write(st.session_state.user_db.getbuffer())
                    st.session_state.df = read_sql_query(st.session_state.sql_query, 'temp_db.sqlite')
                    if st.session_state.df.empty:
                        st.write("""<h4 style="color: #ff3333;">No results found for the given query. Try another 
                            input...!</h4>""",
                                 unsafe_allow_html=True
                                 )
            except:
                st.error(
                    "Could not extract SQL query from the response. Please try again to retrieve data or change the "
                    "input with respect to database.")
                st.stop()
        else:
            st.error("Please enter a valid Question or Prompt related to database.")
            st.stop()

    if not st.session_state.df.empty:
        with st.container():
            st.subheader(":grey[SQL Query:]", anchor=False)
            st.code(st.session_state.sql_query, language='sql')
            st.subheader(":rainbow[Query Results:]", anchor=False)
            st.dataframe(st.session_state.df, use_container_width=True)
            st.write(st.session_state.df.shape)
            st.subheader(":rainbow[Chart Visualization:]", anchor=False)
            col1, col2 = st.columns(2)

        with col1:
            chart_type = st.selectbox("Select Chart Type", ['Bar Chart', 'Line Chart', 'Pie Chart', 'Scatter Chart'])

        with col2:
            x_col = st.selectbox("Select X-axis Column", st.session_state.df.columns)
            y_col = st.selectbox("Select Y-axis Column", st.session_state.df.columns)

        fig = plot_data(st.session_state.df, chart_type, x_col, y_col)
        if fig:
            st.plotly_chart(fig)
