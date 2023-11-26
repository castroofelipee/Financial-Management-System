import streamlit as st
import sqlite3
import pandas as pd


conn = sqlite3.connect('financial_data.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS financial_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount REAL,
        date DATE DEFAULT (datetime('now','localtime'))
    )
''')
conn.commit()


def insert_data(category, amount):
    cursor.execute('INSERT INTO financial_data (category, amount) VALUES (?, ?)', (category, amount))
    conn.commit()


def get_data():
    cursor.execute('SELECT category, SUM(amount) FROM financial_data GROUP BY category')
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['Category', 'Total'])


st.sidebar.title('Financial Management')
selected_option = st.sidebar.radio('Select Option', ['Record Data', 'View Summary'])


if selected_option == 'Record Data':
    st.title('Record Financial Data')
    category = st.selectbox('Select Category', ['Income', 'Expenses', 'Investments'])
    amount = st.number_input('Enter Amount', value=0.0)

    
    if st.button('Submit'):
        insert_data(category, amount)
        st.success('Data recorded successfully!')

elif selected_option == 'View Summary':
    st.title('Financial Summary')

    
    data_summary = get_data()
    st.bar_chart(data_summary.set_index('Category'))

   
    total_income = data_summary[data_summary['Category'] == 'Income']['Total'].values
    total_expenses = data_summary[data_summary['Category'] == 'Expenses']['Total'].values
    total_investments = data_summary[data_summary['Category'] == 'Investments']['Total'].values

    total = (total_income - total_expenses + total_investments)[0] if total_income and total_expenses and total_investments else 0.0

    st.info(f'Total: ${total:.2f}')
