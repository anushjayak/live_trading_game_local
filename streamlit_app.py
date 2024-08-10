import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# Function to connect to the SQLite database and fetch data from a specific table
def get_data_from_table(table_name):
    # Connect to the database
    conn = sqlite3.connect('live_trading_game_db.db')  # Replace 'your_database.db' with your database file
    # Fetch data from the specified table
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    # Close the connection
    conn.close()
    return df

# Function for the database page
def database_page():
    st.title("Database Page")
    
    # Specify the table name
    table_name = "api_keys"  # Replace 'your_table' with your table name
    
    # Get data from the table
    data = get_data_from_table(table_name)
    
    # Display data in Streamlit
    st.dataframe(data, use_container_width=True)

# Sidebar for navigation
page = st.sidebar.selectbox("Select a page", ["Home", "User Performance", "User Details", "Trades", "Database"])

# Render the selected page
if page == "Home":
    st.title("Home Page")
    st.write("Welcome to the Streamlit app.")
elif page == "User Performance":
    st.title("View Users Performance")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data, height=590, use_container_width=True)
elif page == "User Details":
    st.title("View User Details")
    tab1, tab2, tab3 = st.tabs(["Users", "New", "Edit"])

    with tab1:
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
elif page == "Trades":
    st.title("View Trades")
    tab1, tab2 = st.tabs(["Active Orders", "Past Orders"])

    with tab1:
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.dataframe(df, use_container_width=True)

    with tab2:
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.dataframe(df, use_container_width=True)
elif page == "Database":
    database_page()
