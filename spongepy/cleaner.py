# The core logic
import pandas as pd
import numpy as np
import yaml
from .config_loader import use_config, create_config

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

def show_general_stats(df):
    def print_section(title, emoji="📊"):
        print(f"\n\033[1;34m{emoji} {title} {emoji}\033[0m")
        print("\033[1;34m" + "=" * (len(title) * 2 + 4) + "\033[0m")

    print_section("GENERAL DESCRIPTION", "")
    print('\n'.join(str(df.describe()).split('\n')[:-1]))
    print("Number of rows in the Dataset: " , len(df))

    print_section("COLUMNS IN DATASET", "📑")
    print(f"Total Columns: {len(df.columns)}")
    print("\n\033[1mColumn Names:\033[0m")
    print(', '.join(df.columns))

    print_section("MISSING VALUES ANALYSIS", "🔍")
    missing_data = []
    missing_cols = [col for col in df.columns if df[col].isnull().sum() > 0]
    if missing_cols:
        print("\033[1;31mColumns with missing values:\033[0m")
        for col in missing_cols:
            missing_percent = df[col].isnull().mean() * 100

            missing_data.append((col, missing_percent))

            message = ""
            if missing_percent > 55:
                message = f"\033[31m    To be deleted\033[0m"
            elif missing_percent < 5 :
                message = f"\033[33m    Replace missing data with mean\033[0m"

            print(f" - \033[1m{col}\033[0m: {df[col].isnull().sum():,} missing "
                  f"({missing_percent:.1f}%)" + message)
    else:
        print("\033[1;32mNo columns with missing values found!\033[0m")

    missing_data.sort(key=lambda x: x[1], reverse=True)
    first = True
    columns = []
    for col in df.columns:
        columns.append(col)
        if df[col].dtype.kind == "S":
            if first:
                first = False
                print_section("STRING COLUMNS ANALYSIS", "🔤")
            print(f"\n\033[1mColumn: {col}\033[0m")

            unique_chars = set()
            for s in df[col].dropna():
                unique_chars.update(s.decode('utf-8'))

            su = ''.join(sorted([c for c in unique_chars if c.isupper()]))
            sl = ''.join(sorted([c for c in unique_chars if c.islower()]))
            sn = ''.join(sorted([c for c in unique_chars if c.isdigit()]))
            so = ''.join(sorted([c for c in unique_chars if not c.isalnum()]))

            print(f"  Uppercase: \033[35m{su or 'None'}\033[0m")
            print(f"  Lowercase: \033[35m{sl or 'None'}\033[0m")
            print(f"  Numbers:   \033[35m{sn or 'None'}\033[0m")
            print(f"  Special:   \033[35m{so or 'None'}\033[0m")
    
    create_config({
        "columns":     columns,
        "missing-data": missing_data
    })

def primary_cleaning(df):
    df.drop_duplicates(inplace=True)

def missing_data(df, param="default", u_boundary=0.55, d_boundary=0.55):
    for col in df.columns:
        if df[col].isnull().sum() / df[col].value_counts() < d_boundary :
            df[col].dropna(inplace=True)
        elif df[col].isnull().sum() / df[col].value_counts() > u_boundary:
            df.drop(col, axis=1, inplace=True)
        else:
            if param == "default":
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].mean(), inplace=True)