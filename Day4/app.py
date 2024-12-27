'''
import sqlite3 as sql
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Configure the GenAI API
key = os.getenv("GOOGLE_API_KEY")
if not key:
    raise ValueError("API key not found. Please set 'GOOGLE_API_KEY' in your .env file.")
genai.configure(api_key=key)

# Function to initialize the database and insert data
def initialize_database():
    connection = sql.connect("employee.db")
    cursor = connection.cursor()

    # Create table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        empid INT PRIMARY KEY, 
        empname VARCHAR(20), 
        empsalary INT, 
        empdesignation VARCHAR(20)
    )
    """)
    
    # Insert data if the table is empty
    cursor.execute("DELETE FROM employees")  # Ensure no duplicate entries
    cursor.execute("INSERT INTO employees VALUES (1, 'kumar', 100000, 'Developer')")
    cursor.execute("INSERT INTO employees VALUES (2, 'badri', 200000, 'HR')")
    cursor.execute("INSERT INTO employees VALUES (3, 'damo', 30000, 'Manager')")
    cursor.execute("INSERT INTO employees VALUES (4, 'ameer', 40000, 'Realist')")
    
    connection.commit()
    connection.close()

# Function to get SQL query from Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    res = model.generate_content(f"{prompt}\nQuestion: {question}")
    return res.text.strip()

# Function to execute the SQL query
def hit_sql_database(query, db):
    connection = sql.connect(db)
    cursor = connection.cursor()
    try:
        data = cursor.execute(query)
        rows = data.fetchall()
        connection.commit()
        return rows
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return []
    finally:
        connection.close()

# Initialize the database
initialize_database()

# Define the prompt and question
prompt = """
You are an expert in converting natural language questions into SQL queries.
The SQL database 'employee.db' contains a table named 'employees' with the following columns:
- empid
- empname
- empsalary
- empdesignation

For example:
1. To select all columns: SELECT * FROM employees;
2. To select employee names with a salary greater than 10000: SELECT empname FROM employees WHERE empsalary > 10000;

Your task is to generate an SQL query based on the question below without including 'SQL' in the output or enclosing the query in quotes.
"""

# Streamlit app setup
st.set_page_config(page_title="Prompt to SQL")
st.header("Gemini Application for Text-SQL")

questionW = st.text_input("Input:", key="input")

submit = st.button("Ask me any questions")

if submit:
    res = get_gemini_response(questionW, prompt)
    print("Generated SQL query:", res)
    data = hit_sql_database(res, "employee.db")
    st.subheader("The response is")
    st.header("Query for the Input")
    st.write(res)
    st.header("Result of the Query")   
    for row in data:
        row_str = ', '.join(map(str, row))  # Convert tuple to string
        print(row_str)
        st.write(row_str)

        '''
import sqlite3 as sql
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st
import logging
import pandas as pd

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Configure the GenAI API
key = os.getenv("GOOGLE_API_KEY")
if not key:
    raise ValueError("API key not found. Please set 'GOOGLE_API_KEY' in your .env file.")
genai.configure(api_key=key)

# Function to initialize the database and insert data
def initialize_database():
    connection = sql.connect("employee.db")
    cursor = connection.cursor()

    # Create table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        empid INT PRIMARY KEY, 
        empname VARCHAR(20), 
        empsalary INT, 
        empdesignation VARCHAR(20)
    )
    """)
    
    # Insert data if the table is empty
    cursor.execute("DELETE FROM employees")  # Ensure no duplicate entries
    cursor.execute("INSERT INTO employees VALUES (1, 'John', 100000, 'Developer')")
    cursor.execute("INSERT INTO employees VALUES (2, 'Clarke', 200000, 'HR')")
    cursor.execute("INSERT INTO employees VALUES (3, 'Bob', 30000, 'Manager')")
    cursor.execute("INSERT INTO employees VALUES (4, 'Smith', 40000, 'Ethical Hacker')")
    
    connection.commit()
    connection.close()

# Function to get SQL query from Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    res = model.generate_content(f"{prompt}\nQuestion: {question}")
    return res.text.strip()

# Function to execute the SQL query
def hit_sql_database(query, db):
    connection = sql.connect(db)
    cursor = connection.cursor()
    try:
        data = cursor.execute(query)
        rows = data.fetchall()
        connection.commit()
        return rows
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return []
    finally:
        connection.close()

# Initialize the database
initialize_database()

# Define the prompt and question
prompt = """
You are an expert in converting natural language questions into SQL queries.
The SQL database 'employee.db' contains a table named 'employees' with the following columns:
- empid
- empname
- empsalary
- empdesignation

For example:
1. To select all columns: SELECT * FROM employees;
2. To select employee names with a salary greater than 10000: SELECT empname FROM employees WHERE empsalary > 10000;

Your task is to generate an SQL query based on the question below without including 'SQL' in the output or enclosing the query in quotes.
"""

# Streamlit app setup
st.set_page_config(page_title="Prompt to SQL")
st.header("Gemini Application for Text-SQL")

questionW = st.text_input("Input:", key="input")

submit = st.button("Ask me any questions")

if submit:
    res = get_gemini_response(questionW, prompt)
    st.header("Query for the Input")
    st.write(res)
    
    data = hit_sql_database(res, "employee.db")
    
    st.header("Result of the Query")
    
    if data:
        # Fetch column names from the database
        connection = sql.connect("employee.db")
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(employees)")
        columns = [column[1] for column in cursor.fetchall()]  # Extract column names
        connection.close()

        # Create a DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Display the DataFrame as a table
        st.dataframe(df)  # Interactive table
    else:
        st.write("No data returned for the given query.")
