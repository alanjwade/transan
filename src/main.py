import pandas as pd
import re
import os

# Read all CSV files in the bank_transactions directory into a list of DataFrames
transaction_files = [pd.read_csv(os.path.join('data/bank_transactions', f)) for f in os.listdir('data/bank_transactions') if f.endswith('.csv')]

# Concatenate all DataFrames into a single DataFrame
transactions_df = pd.concat(transaction_files, ignore_index=True)

# Read the payee_list.csv file into a DataFrame
payee_list_df = pd.read_csv('data/mappings/payee_list.csv')

# Function to map 'Payee' and 'Category' based on 'Description'
def map_payee_category(description):
    for _, row in payee_list_df.iterrows():
        if re.search(row['Orig Desc'], description, re.IGNORECASE):
            return pd.Series([row['Payee'], row['Category']])
    return pd.Series([None, None])

# Apply the function to the 'Description' column
transactions_df[['Payee', 'Category']] = transactions_df['Description'].apply(map_payee_category)

# Display the resulting DataFrame
print(transactions_df.head())