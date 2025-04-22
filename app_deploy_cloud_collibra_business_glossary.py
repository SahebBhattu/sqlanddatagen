
#from dotenv import load_dotenv
#load_dotenv() ## load all the environemnt variables

import streamlit as st

import os
import sqlite3
import numpy as np
import pandas as pd
import sqlitecloud
#from google.colab import userdata
import google.generativeai as genai
## Configure Genai Key



# Add custom CSS to hide the GitHub icon


os.environ['GOOGLE_API_KEY'] = "AIzaSyCvxW1W7vVcaXVgqZGu_P6CIRHopQd42NE"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])


## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro-latest')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql):
    conn=sqlitecloud.connect("sqlitecloud://cbz5elionk.g1.sqlite.cloud:8860/Consumer_test1.db?apikey=73AjvC1jb2D2iU8b7ooP0ePONdYkQGaKbL5jbeTeOvA")
    cursor=conn.execute(sql)
    print("In the function")
    rows=cursor.fetchall()
    #conn.commit()
    #conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """    You are an expert in converting English questions to SQL query!
    The SQL database has the name Customers and has the following columns - CustomerID,CustomerName,ContactName,Address,City,PostalCode,Country,Income, InsurancePlan
    The SQL database has the name Payout and has the following columns - Annuity_category_ID, CustomerID, EmployeeID, Payout_Date, Payment_cycle_ID
    The tables Customers and Payout can be joined on CustomerID column of Customers table and CustomerID column of Orders table
     \n\nFor example,\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM Customers ;
    \nExample 2 - Tell me all the Customers located in USA?,
    the SQL command will be something like this SELECT CustomerName, Country FROM Customers
    where Country="UK";
    Annuity_category_ID can be treaded as Annuity category ID or type of Annuity category
    Payout_Date can be treated as Payout Date 
    Payment_cycle_ID can be treated as Payment cycle ID
    InsurancePlan can be treated as insurance plan OR insurance_plan
    CustomerID can be treated as Customer ID
    Also the sql code should not have ``` in beginning or end and sql word in output
    only an executable SQL should be returned in the response
    don't add ';' at the end
    don't add '```sql' at the beginning , only an executable SQL query in the response
    don't use DESCRIBE keyword
    
"""


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("GenAI SQL Query And Data Generator Complete Application")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question for retriving information from the database")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    st.header("The generated SQL query is")
    st.subheader(response)
    response = response.replace(";", "")
    print(response)
    response_data=read_sql_query(response)
    print(response_data)
    st.header("The generated output is")
    for row in response_data:
        print(row)
        st.subheader(row)
