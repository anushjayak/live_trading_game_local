import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import requests

def get_data_from_table(table_name):
    conn = sqlite3.connect('database.db')  # Replace with your database file
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def save_api_key(user_id, api_key):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO api_keys (user_id, api_key) VALUES (?, ?)", (user_id, api_key))
    conn.commit()
    conn.close()

def fetch_trades(api_key):
    url = "https://api.trading212.com/api/v1/equity/orders"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        trades = response.json()

        if trades:  # Check if there is any trade data
            df = pd.DataFrame(trades)
            return df
        else:
            st.write("No trades found.")
            return pd.DataFrame()
    else:
        # Handle errors
        st.error(f"Failed to fetch trades. Status Code: {response.status_code}. Response: {response.text}")
        return pd.DataFrame()




def home_page():
    st.title("Home Page")
    st.write("Welcome to the Trading Performance Tracker app.")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=300)  # Example image, replace as needed



def api_key_submission_page():
    st.title("Submit Your API Key")
    user_id = st.text_input("Enter your User ID:")
    api_key = st.text_input("Enter your Trading 212 API Key:", type="password")

    if st.button("Submit"):
        if user_id and api_key:
            save_api_key(user_id, api_key)
            st.success("API Key submitted successfully!")
        else:
            st.error("Please enter both User ID and API Key.")

def user_performance_page():
    st.title("User Performance")
    user_id = st.text_input("Enter your User ID to fetch performance:")

    if st.button("Fetch Performance"):
        # Fetch API key for the user from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.execute("SELECT api_key FROM api_keys WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            api_key = row[0]
            trades_df = fetch_trades(api_key)
            if not trades_df.empty:
                st.dataframe(trades_df)
            else:
                st.write("No trades found or failed to fetch trades.")
        else:
            st.error("API key not found for the user. Please submit your API key first.")



def trades_page():
    st.title("View Trades")
    user_id = st.text_input("Enter your User ID to view trades:")

    if st.button("View Trades"):
        # Fetch API key for the user from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.execute("SELECT api_key FROM api_keys WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            api_key = row[0]
            trades_df = fetch_trades(api_key)
            if not trades_df.empty:
                st.dataframe(trades_df)
            else:
                st.write("No trades found or failed to fetch trades.")
        else:
            st.error("API key not found for the user. Please submit your API key first.")



def database_page():
    st.title("Database Page")
    table_name = "api_keys"  # Replace with your table name
    data = get_data_from_table(table_name)
    st.dataframe(data, use_container_width=True)


page = st.sidebar.selectbox("Select a page", ["Home", "Submit API Key", "User Performance", "Trades", "Database"])

if page == "Home":
    home_page()
elif page == "Submit API Key":
    api_key_submission_page()
elif page == "User Performance":
    user_performance_page()
elif page == "Trades":
    trades_page()
elif page == "Database":
    database_page()
