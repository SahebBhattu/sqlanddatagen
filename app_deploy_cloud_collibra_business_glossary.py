
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
    ##model=genai.GenerativeModel('gemini-1.5-pro-latest')
    model=genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql):
    conn=sqlitecloud.connect("sqlitecloud://cbz5elionk.g1.sqlite.cloud:8860/Consumer_test2_encrypted.db?apikey=73AjvC1jb2D2iU8b7ooP0ePONdYkQGaKbL5jbeTeOvA")
    cursor=conn.execute(sql)
    print("In the function")
    rows=cursor.fetchall()
    #conn.commit()
    #conn.close()
    for row in rows:
        print(row)
    return rows


def read_sql_query_output(query):
    conn = sqlitecloud.connect("sqlitecloud://cbz5elionk.g1.sqlite.cloud:8860/Consumer_test2_encrypted.db?apikey=73AjvC1jb2D2iU8b7ooP0ePONdYkQGaKbL5jbeTeOvA")  # replace with your DB path or connection
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return columns, rows




def get_columns_list(table_name):
    #response=get_gemini_response(question,prompt)
    response = "LIST METADATA TABLE "+table_name
    response_data=read_sql_query(response)
    #print("hello ")
    #print(str(response_data));
    metadata = [str(response_data)]
    #print(metadata)
    metadata = str(', '.join([col[0] for col in response_data]))
    print(metadata)
    return metadata




def get_collibra_business_glossary():
    response = "Select name, definition from collibra_business_glossary"
    response_data=read_sql_query(response)
    print("hello")
    #print(response_data);
    #metadata = [str(response_data)]
    #print(metadata)
    collibra_business_glossary = "    \n".join([f"{column} = {description}" for column, description in response_data])
    return collibra_business_glossary







## Define Your Prompt
prompt_non_active=[
    """    You are an expert in converting English questions to SQL query!
    The SQL database has a table named Customers and it has the following columns - Cust_ID,Cust_Nam,Contact_Nam,Add,City,P_Code,Ctry,IC, Ins_Plan
    The SQL database has a table named Payout and it has the following columns - Annuity_category_ID, CustomerID, EmployeeID, Payout_Date, Payment_cycle_ID

    ------------------------------------------------------------------------------------------------------------
    Please understand this business glossary while converting prompt input into actual column names of the table Customers:
    It is given as 
    actual column name = business glossary description
    Cust_ID = It is a Customer ID 
    Cust_Nam = It is a Customer's name
    Contact_Nam = It is Contact Name
    Add = It is Address of the customer
    City = It is city where the customer lives
    P_Code =  It is Postal code of that city
    Ctry = It is the Country of the customer
    IC = It is the Income of the customer
    Ins_Plan = It is the Insurance Plan opted by the customer 
    ------------------------------------------------------------------------------------------------------------
    
    
    
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

prompt=[
    """    You are an expert in converting English questions to SQL query!
    The SQL database has the name Customers and has the following columns - """+get_columns_list("Customers")+""" 
    The SQL database has the name Payout and has the following columns - Annuity_category_ID, CustomerID, EmployeeID, Payout_Date, Payment_cycle_ID

    ------------------------------------------------------------------------------------------------------------
    Business Glossary
    Please understand this business glossary while converting prompt input into actual column names of the table Customers:
    It is given as 
    actual column name = business glossary description
    """+get_collibra_business_glossary()+"""
    ------------------------------------------------------------------------------------------------------------
    
    
    
    
    
     \n\nFor example,\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM Customers ;
    \nExample 2 - Tell me all the Customers located in UK?
    the SQL command will be something like this SELECT Customer's Name, Country FROM Customers
    where Country="UK";

    Table joins:
    The tables Customers and Payout can be joined on Customer ID column of Customers table and Customer ID column of Payout table
    example:
    Find the customer who is from London and Payment cycle ID is 2
    The SQL query will be like this
    SELECT * FROM Customers
    JOIN Payout ON Customers.customer ID = Payout.customer ID
    WHERE City = 'London'
    AND Payment cycle ID = 2;

    Please always refer the Business Glossary before generating every SQL so that the right column names will get picked.

    
    Annuity_category_ID can be treaded as Annuity category ID or type of Annuity category
    Payout_Date can be treated as Payout Date 
    Payment_cycle_ID can be treated as Payment cycle ID
    InsurancePlan can be treated as insurance plan OR insurance_plan
    CustomerID can be treated as Customer ID

    Please always refer the Business Glossary before generating every SQL so that the right column names will get picked.

    
    Also the sql code should not have ``` in beginning or end and sql word in output
    only an executable SQL should be returned in the response
    don't add ';' at the end
    don't add '```sql' at the beginning , only an executable SQL query in the response
    don't use DESCRIBE keyword

    
    
"""


]

## Streamlit App

st.set_page_config(page_title="Query and Data Gen")
st.header("GenAI SQL Query And Data Generator Complete Application_Collibra")

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
    st.dataframe(response_data)
    for row in response_data:
        print(row)
        st.subheader(row)
