from dotenv import load_dotenv
import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Google API Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database Path Configuration
database_path = 'netflix_data.db'

# Function to get response from the Generative Model API
def get_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL query and return results as DataFrame
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# Function to plot data
def plot_data(df, chart_type, x_col, y_col):
    if chart_type == 'Bar Chart':
        fig = px.bar(df, x=x_col, y=y_col)
    elif chart_type == 'Line Chart':
        fig = px.line(df, x=x_col, y=y_col)
    elif chart_type == 'Pie Chart':
        fig = px.pie(df, names=x_col, values=y_col)
    elif chart_type == 'Scatter Chart':
        fig = px.scatter(df, x=x_col, y=y_col)
    else:
        st.write("Unsupported chart type")
        return None
    return fig

# Prompt for the Generative Model
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name netflix_data and it has 5 tables named as netflix, netflix_cast, netflix_country, netflix_directors, netflix_genre.
    The netflix table has following columns - show_id, type, title, date_added, release_year, rating, duration, description \n\nThe netflix_cast table has following columns - show_id, cast \n\nThe netflix_country table has following columns - show_id, country \n\nThe netflix_directors table has following columns - show_id, director \n\nThe netflix_genre table has following columns - show_id, genre \n\n
    For example,\nExample 1 - How many entries of records are present in particular table?, 
    the SQL command will be something like this SELECT COUNT(*) FROM netflix ;
    \nExample 2 - Tell me all the title which was released in 2018?, 
    the SQL command will be something like this SELECT * FROM netflix 
    where release_year="2018"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    All 5 tables have common show_id column which will be reference as key to interlinked the records to retrieve data from a query
    """
]

# Store DataFrame in session state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'sql_query' not in st.session_state:
    st.session_state.sql_query = ''

def click_button():
    st.session_state.clicked = True


# Streamlit web interface configuration
st.set_page_config(page_title="SQL Query Generator and Visualization Web App", layout="wide", page_icon='📊')

st.markdown("""
     <h1 style="color: DarkOrange; text-align: center; width: 100%;">
     📊 DataQuery Pro: Retrieve Data with Ease
     </h1>
     """, unsafe_allow_html=True
)

with st.container():
    st.subheader(":rainbow[QUERY PLAYGROUND]", anchor=False)
    col1, col2 = st.columns([6, 1], gap="small", vertical_alignment="bottom")
    with col1:
        question = st.text_input(":orange[Input your question here:]", key="input", placeholder="Type here...")
    with col2:
        submit = st.button("Get Data", help="Click to submit your question.", on_click=click_button)

if submit:
    if question:
        st.session_state.sql_query = get_response(question, prompt)
        try:
            if st.session_state.sql_query:
                st.session_state.df = read_sql_query(st.session_state.sql_query, database_path)
                if st.session_state.df.empty:
                    st.write("""<h4 style="color: #ff3333;">No results found for the given query. Try another input...!</h4>""", 
                    unsafe_allow_html=True)
        except:
            st.error("Could not extract SQL query from the response. Please try again to retrieve data or change the input with respect to database.")
            st.stop()
    else:
        st.error("Please enter a valid Question related to database.")
        st.stop()

if not st.session_state.df.empty:
    with st.container():
        st.subheader(":grey[SQL Query:]", anchor=False)
        st.code(st.session_state.sql_query, language='sql')
        st.subheader(":rainbow[Query Results:]", anchor=False)
        st.dataframe(st.session_state.df)  
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
