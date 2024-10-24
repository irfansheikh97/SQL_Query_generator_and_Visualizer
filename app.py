import streamlit as st
import pandas as pd
import google.generativeai as genai
from model_methods import get_response, plot_data, read_sql_query, check_api_key
from views.about_page import about_app

# Streamlit web interface configuration
st.set_page_config(page_title="Query Data Pro", layout="wide", page_icon='📊')

st.markdown("""<h1 style=" text-align: center; color: #FF2400;">Query Data Pro: Upload📁 Ask❓ Visualize📈</h1> """, unsafe_allow_html=True)

@st.experimental_dialog("About App", width="large")
def show_about_app():
    about_app()


# streamlit session state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'sql_query' not in st.session_state:
    st.session_state.sql_query = ''

if 'db' not in st.session_state:
    st.session_state.db = None

if 'prompt' not in st.session_state:
    st.session_state.prompt = ""


def click_button():
    st.session_state.clicked = True


user_database = None

# /*---- New code start ----*/
with st.sidebar:
    st.logo("assets/logo.png")
    if st.button("About the App", use_container_width=True):
        show_about_app()

    gemini_api_key = st.text_input(label=":key: Enter Gemini API Key :", type='password',
                                   key='api_key')
    if st.session_state.api_key != '':
        try:
            is_valid = check_api_key(gemini_api_key)
            if is_valid:
                st.success("Gemini API Key is valid...!")
                genai.configure(api_key=gemini_api_key)
                user_database = st.file_uploader(":open_file_folder: Upload your database file",
                                     type=[".sqlite", '.db', '.sql'], key='db')
        except:
            st.error("Please pass a valid API key.")

if user_database is not None:
    with st.container():
        # Prompt for the Generative Model
        prompt = st.text_area(":keyboard: Enter a Prompt for Model:", height=200,
                      help="Enter the prompt for AI model to interact with"
                           "your database file. Basically a role of SQL "
                           "Expert/Developer.", key='prompt')
        st.subheader(":rainbow[QUERY PLAYGROUND]", anchor=False)
        question = st.text_input("Input your question here: ", key="input", placeholder="Type here...")
        submit = st.button("Get Data", help="Click to submit your question.", on_click=click_button)
    
    with st.spinner():
        if submit:
            if question and prompt:
                st.session_state.sql_query = get_response(question, prompt)
                try:
                    if st.session_state.sql_query:
                        # Write the uploaded file to a temporary location
                        with open('temp_db.sqlite', 'wb') as f:
                            f.write(user_database.getbuffer())
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
                st.subheader(":rainbow[SQL Query:]", anchor=False)
                st.code(st.session_state.sql_query, language='sql')
                st.subheader(":rainbow[Query Results:]", anchor=False)
                st.dataframe(st.session_state.df, use_container_width=True, hide_index=True)
                st.write("Dataframe has:", st.session_state.df.shape[0], "Rows", "and", st.session_state.df.shape[1],
                        "Columns")
            
            if len(st.session_state.df.columns) > 1:
                st.subheader(":rainbow[Chart Visualization:]", anchor=False)

                col1, col2 = st.columns(2)
                with col1:
                    chart_type = st.selectbox("Select Chart Type", ['Bar Chart', 'Line Chart', 'Pie Chart', 'Scatter Chart'])

                with col2:
                    x_col = st.selectbox("Select X-axis Column", st.session_state.df.columns)
                    y_col = st.selectbox("Select Y-axis Column", st.session_state.df.columns)

                fig = plot_data(st.session_state.df, chart_type, x_col, y_col)
                if fig:
                    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
            else:
                st.write("DataFrame has only 1 column, Please try generating 2 or more columns DataFrame")
