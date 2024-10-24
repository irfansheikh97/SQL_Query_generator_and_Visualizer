import streamlit as st


def about_app():
    # --- Title and Description ---
    st.write("\n")
    # st.title(":red[Query Data Pro]", anchor=False)
    st.markdown("""<h1 style=" text-align: center; color: #FF2400;">Query Data Pro</h1> """, unsafe_allow_html=True)
    st.write(
        """This app allows users to upload database files (.sqlite, .db, .sql) and interact with them using natural 
        language queries. The app leverages a Large Language Model (LLM) to convert user questions into SQL queries and 
        chart Visualizer and retrieve relevant data from the uploaded database. The app is designed with a user-friendly 
        interface and is hosted using Streamlit."""
    )

    # --- Features ---
    st.write("\n")
    st.subheader("Features", anchor=False)
    st.write(
        """
        - <b style="color: #FF2400;">Database Upload</b>: Users can upload .sqlite, .db, or .sql files directly from their local system.
        - <b style="color: #FF2400;">Natural Language Query</b>: Users can input natural language questions, which the app converts into SQL queries to fetch data from the database.
        - <b style="color: #FF2400;">Interactive Output</b>: The results of the SQL queries are displayed in a tabular format and using Different chart Visualizer, allowing users to explore the data interactively.
        - <b style="color: #FF2400;">Gemini API Integration</b>: The app integrates with the Gemini LLM via API to convert questions into SQL queries intelligently.
        - <b style="color: #FF2400;">Session State Management</b>: Uploaded database files are stored in session state to persist across user interactions, ensuring smooth workflow without re-uploading files.
        """, unsafe_allow_html=True
    )

    # --- Working Guide ---
    st.write("\n")
    st.subheader("How It Works", anchor=False)
    st.write(
        """
        - <b style="color: #FF2400;">Provide Gemini API Key</b>: Users must provide their API key for the Gemini model to enable question-to-SQL conversion.
        - <b style="color: #FF2400;">Upload a Database File</b>: Users can upload database file (.db, .sqlite, .sql).
        - <b style="color: #FF2400;">Input a Prompt</b>: Users enter a prompt to define the role of the AI model (e.g., "SQL expert").
        - <b style="color: #FF2400;">Ask a Question</b>: Users ask questions related to the data in natural language (e.g., "What is the average price of products?").
        - <b style="color: #FF2400;">Data Retrieval</b>: The app converts the question into a SQL query, executes it on the uploaded database, and returns the results.
        - <b style="color: #FF2400;">View Results</b>: The resulting data is displayed in a table for easy analysis and using chart visualiser the data can be viewed in charts/plots format.
        """, unsafe_allow_html=True
    )

