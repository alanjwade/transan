import pandas as pd
import re

def rolling_12_month_average(df):
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort the dataframe by date
    df = df.sort_values('Date')
    
    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)
    
    # Calculate the rolling 12 month average of the 'Amount' column
    df['12_month_avg'] = df['Amount'].rolling(window=12, min_periods=1).mean()
    
    return df

# # Example usage
# if __name__ == "__main__":
#     data = {
#         'Date': ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01', 
#                  '2021-07-01', '2021-08-01', '2021-09-01', '2021-10-01', '2021-11-01', '2021-12-01'],
#         'Description': ['desc1', 'desc2', 'desc3', 'desc4', 'desc5', 'desc6', 'desc7', 'desc8', 'desc9', 'desc10', 'desc11', 'desc12'],
#         'Amount': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
#         'Account': ['acc1', 'acc2', 'acc3', 'acc4', 'acc5', 'acc6', 'acc7', 'acc8', 'acc9', 'acc10', 'acc11', 'acc12'],
#         'Tag': ['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7', 'Tag8', 'Tag9', 'Tag10', 'Tag11', 'Tag12']
#     }
    
#     df = pd.DataFrame(data)
#     result = rolling_12_month_average(df)
#     print(result)

def monthly_totals(data):

 
    # Exclude transactions with 'exclude_investment' in the 'Tag' column
    data = data[~data['Tag'].fillna('').str.contains('#exclude_investment', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#ccpayment', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#colege529', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#IBondRedemption', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#exclude', flags=re.IGNORECASE, regex=True)]

    # Group transactions by month
    data['month'] = data['Date'].dt.to_period('M')

    monthly_transactions = data.groupby('month')
    for month, transactions in monthly_transactions:
        # print(f"Month: {month}")
        # print(transactions)
        monthly_sum = transactions['Amount'].sum()
        income_sum = transactions['Income'].sum()
        expense_sum = transactions['Expense'].sum()

        print(f"Total for {month}: {monthly_sum:>10,.2f} (Income: {income_sum:>10,.2f}, Expense: {expense_sum:>10,.2f})")

def rolling_12_month_average(data, column='Amount'):
    # Exclude transactions with 'exclude_investment' in the 'Tag' column
    data = data[~data['Tag'].fillna('').str.contains('#exclude_investment', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#ccpayment', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#colege529', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#IBondRedemption', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#exclude_car', flags=re.IGNORECASE, regex=True)]
    data = data[~data['Tag'].fillna('').str.contains('#exclude_Janet529', flags=re.IGNORECASE, regex=True)]


    # Ensure the 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Group transactions by month
    data['month'] = data['Date'].dt.to_period('M')

    monthly_transactions = data.groupby('month')
    
    # Calculate the rolling 12 month average for the specified column
    monthly_sums = monthly_transactions[column].sum().reset_index()
    monthly_sums['rolling_12_month_avg'] = monthly_sums[column].rolling(window=12, min_periods=1).mean()
    monthly_sums[column] = monthly_sums[column].apply(lambda x: f"{x:.2f}")
    monthly_sums['rolling_12_month_avg'] = monthly_sums['rolling_12_month_avg'].apply(lambda x: f"{x:.2f}")
    print(monthly_sums)

    return monthly_sums

def list_of_categories(data):
    # Get unique categories from the 'Category' column
    categories = data['Category'].unique()
    return categories