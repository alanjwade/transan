# src/data/loader.py
import pandas as pd
import numpy as np
from pathlib import Path

class BankDataLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.mapping_file = data_dir['mappings'] / "category_mapping.csv"
        self.trans_mapping_file = data_dir['mappings'] / "transaction_mapping.csv"
    
    def load_statement(self, file: Path) -> pd.DataFrame:
        if file.name.startswith('DC_'):
            df = pd.read_csv(file.as_posix(), parse_dates=['Trans. Date'])
            df['Trans. Date'] = pd.to_datetime(df['Trans. Date'])
            df = df.rename(columns={'Trans. Date': 'Date', 'Description': 'Description', 'Amount': 'Amount'})
            df['Account'] = 'Discover'
            df['Amount'] = -df['Amount']  # Invert the 'Amount' column
        elif file.name.startswith('FT_'):
            df = pd.read_csv(file.as_posix())
            df['Posting Date'] = pd.to_datetime(df['Posting Date'])
            df = df.rename(columns={'Posting Date': 'Date', 'Description': 'Description', 'Amount': 'Amount'})
            df['Account'] = 'First Tech'
        else:
            return None
        df = self.apply_mapping(df)
        df = self.apply_trans_mapping(df)
        df = self.split_category(df)
        df = self.create_income_expense_col(df)
        df = df[['Date', 'Description', 'Amount', 'Income', 'Expense', 
                    'Category', 'Category1',  'Category2', 'Category3','Account', 'Tag']]  # Keep only the specified columns
        return df
        
    def create_income_expense_col(self, data: pd.DataFrame) -> pd.DataFrame:
        data['Income'] = data['Amount'].apply(lambda x: x if x > 0 else 0)
        data['Expense'] = data['Amount'].apply(lambda x: x if x < 0 else 0)
        return data
    
    
    def load_mapping(self) -> dict:
        mapping_df = pd.read_csv(self.mapping_file.as_posix())
        return mapping_df
    
    def load_trans_mapping(self) -> dict:
        mapping_df = pd.read_csv(self.trans_mapping_file.as_posix(), dtype={'Amount': float})
        return mapping_df
   
    def split_category(self, data: pd.DataFrame) -> pd.DataFrame:
        category_split = data['Category'].str.split(':', expand=True)
        data['Category1'] = category_split[0]
        data['Category2'] = category_split[1] if category_split.shape[1] > 1 else pd.NA
        data['Category3'] = category_split[2] if category_split.shape[1] > 2 else pd.NA
        return data
    
    def load_statements(self) -> pd.DataFrame:
        '''Load all statements from the raw directory'''
        all_files = self.data_dir['raw']
        all_statements = []
        for file in all_files.iterdir():
            if file.is_file():
                statement = self.load_statement(file)
                if statement is not None:
                    all_statements.append(statement)
        all_statements_df = pd.concat(all_statements, ignore_index=True).sort_values(by='Date')
        return all_statements_df
    
    def dump_intermediate(self, data: pd.DataFrame, filename: str):
        data.to_csv(self.data_dir['processed'] / filename, index=False)

    
    def apply_mapping(self, data: pd.DataFrame) -> pd.DataFrame:
        mapping_df = self.load_mapping()
        mapping = dict(zip(mapping_df['Orig Desc'], zip(mapping_df['New Desc'], mapping_df['Category'], mapping_df['Tag'])))
        
        def map_description_and_category(description, amount):
            for orig_desc, (new_desc, category, tag) in mapping.items():
                if orig_desc in description:
                    return new_desc, category, tag
            return description, 'Income:Unassigned:Unassigned' if amount > 0 else 'Expense:Unassigned:Unassigned', None
        
        data[['Description', 'Category', 'Tag']] = data.apply(
            lambda row: map_description_and_category(row['Description'], row['Amount']), axis=1, result_type='expand'
        )

        return data

    def apply_trans_mapping(self, data: pd.DataFrame) -> pd.DataFrame:
        trans_mapping_df = self.load_trans_mapping()
        
        for _, trans_row in trans_mapping_df.iterrows():
            mask = (data['Date'] == pd.to_datetime(trans_row['Date'])) & (np.isclose(data['Amount'].astype(float), float(trans_row['Amount'])))
            data.loc[mask, 'Description'] = trans_row['New Desc']
            data.loc[mask, 'Category'] = trans_row['Category']
            data.loc[mask, 'Tag'] = trans_row['Tag']
        return data