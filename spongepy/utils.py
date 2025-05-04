#utilities for the project
import pandas as pd

def primary_cleaning(df):
    df.drop_duplicates(inplace=True)

def fill_missing_data(df, u_boundary=0.80, d_boundary=0.05):
    for col in df.columns:
        if df[col].isnull().sum() / df[col].value_counts() < d_boundary :
            df[col].dropna(inplace=True)
        elif df[col].isnull().sum() / df[col].value_counts() > u_boundary:
            df.drop(col, axis=1, inplace=True)
        else:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].mean(), inplace=True)

def fix_phone_number(df, col):
    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^\d+\-\s]', '', x))

def fix_name(df, col):
    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^a-zA-Z\s]', ' ', re.sub(r'\d+', '', x)))

def read_into_df(file, param=""):
    suffix = file.split('.')[-1].lower()
    print("Working on file with " + suffix + " extension")
    try:
        if suffix in ['csv', 'txt']:
            return pd.read_csv(file)
        elif suffix in ['xlsx', 'xls']:
            return pd.read_excel(file)
        elif suffix == 'json':
            return pd.read_json(file)
        elif suffix == 'parquet':
            return pd.read_parquet(file)
        elif suffix == 'feather':
            return pd.read_feather(file)
        elif suffix == 'dta':
            return pd.read_stata(file)
        elif suffix == 'pkl':
            return pd.read_pickle(file)
        elif suffix in ['db', 'sqlite']:
            from sqlite3 import connect
            conn = connect(file)
            return pd.read_sql(f"SELECT * FROM {param}", conn)
        else:
            raise ValueError(f"Unsupported file format: .{suffix}")

    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def fix_id_column(df, col):
    if col not in df:
        return
    df.drop_duplicates(subset=[col], inplace=True)
    df.dropna(subset=[col], inplace=True)
    df[col] = df[col].astype(int)

def construct_id_column(df, col):
    if col not in df.columns or df[col].isnull().all():
        df[col] = range(1, len(df) + 1)
