import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai


def check_api_key(api_key: str) -> bool:
    '''
    Function to check whether the API key is valid.
    '''
    if len(api_key) != 0:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        if response:
            return True
        else:
            return False


# Function to get response from the Generative Model API
def get_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
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
        st.error("Unsupported chart type")
        return None
    return fig
