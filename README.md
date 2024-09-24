# SQL Query generator and Visualizer 

This app allows users to upload database files (.sqlite, .db, .sql) and interact with them using natural language queries. The app leverages a Large Language Model (LLM) to convert user questions into SQL queries and chart Visualizer and retrieve relevant data from the uploaded database. The app is designed with a user-friendly interface and is hosted using Streamlit.

## Features
- Database Upload: Users can upload .sqlite, .db, or .sql files directly from their local system.
- Natural Language Query: Users can input natural language questions, which the app converts into SQL queries to fetch data from the database.
- Interactive Output: The results of the SQL queries are displayed in a tabular format and using Different chart Visualizer, allowing users to explore the data interactively.
- Gemini API Integration: The app integrates with the Gemini LLM via API to convert questions into SQL queries intelligently.
- Session State Management: Uploaded database files are stored in session state to persist across user interactions, ensuring smooth workflow without re-uploading files.

## How It Works
- Provide Gemini API Key: Users must provide their API key for the Gemini model to enable question-to-SQL conversion.
- Upload a Database File: Users can upload database file (.db, .sqlite, .sql).
- Input a Prompt: Users enter a prompt to define the role of the AI model (e.g., "SQL expert").
- Ask a Question: Users ask questions related to the data in natural language (e.g., "What is the average price of products?").
- Data Retrieval: The app converts the question into a SQL query, executes it on the uploaded database, and returns the results.
- View Results: The resulting data is displayed in a table for easy analysis and using chart visualiser the data can be viewed in charts/plots format.
- 
App link --> <a href="https://sqlquerygeneratorandvisualizer.streamlit.app">click here</a>


## 🚀 Getting Started

To run the SQL_Query_generator_and_Visualizer locally, follow these steps:

1. Clone the repository: `git clone project_directory
2. Navigate to the project directory: `cd project_directory`
3. Install dependencies:
     ```
     pip install -r requirements.txt
     ```
4. Run the streamlit app:
    ```streamlit run app.py```

5. Start input the questions to the database
6. For sample questions see sample.txt file
