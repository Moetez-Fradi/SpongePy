#utilities for the project
import os
import pandas as pd
from sqlite3 import connect
import re

def primary_cleaning(df):
    df.drop_duplicates(inplace=True)

def fill_missing_data(df, u_boundary=0.80, d_boundary=0.05):
    for col in df.columns:
        miss_frac = df[col].isnull().mean()
        if miss_frac < d_boundary:
            df.dropna(subset=[col], inplace=True)
        elif miss_frac > u_boundary:
            df.drop(col, axis=1, inplace=True)
        else:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].mean(), inplace=True)

def fix_phone_number(df, col):
    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^\d+\-\s]', '', x))

def fix_name(df, col):
    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^a-zA-Z\s]', ' ', re.sub(r'\d+', '', x)))

def write_from_df(df, original_file, export=None, table_name="data"):
    """
    Write `df` out to disk.
    
    - `original_file`: the path the data was read from; used to infer default extension.
    - `export`:  
        • None        → writes to "Sponged_data.<ext>"  
        • "foo"       → writes to "foo.<ext>"  
        • "foo.bar"   → writes to "foo.bar" (honors provided ext)
    - `table_name`: only used if writing to a .db/.sqlite
    """
    orig_ext = os.path.splitext(original_file)[1].lstrip(".").lower()
    
    if export:
        name, ext = os.path.splitext(export)
        if ext:                   
            out_fname = export
            out_ext   = ext.lstrip(".").lower()
        else:                     
            out_fname = f"{export}.{orig_ext}"
            out_ext   = orig_ext
    else:
        out_ext   = orig_ext
        out_fname = f"Sponged_data.{out_ext}"

    if out_ext in ("csv", "txt"):
        df.to_csv(out_fname, index=False)
    elif out_ext in ("xlsx", "xls"):
        df.to_excel(out_fname, index=False)
    elif out_ext == "json":
        df.to_json(out_fname, orient="records", lines=False)
    elif out_ext == "parquet":
        df.to_parquet(out_fname, index=False)
    elif out_ext == "feather":
        df.to_feather(out_fname)
    elif out_ext == "dta":
        df.to_stata(out_fname)
    elif out_ext == "pkl":
        df.to_pickle(out_fname)
    elif out_ext in ("db", "sqlite"):
        conn = connect(out_fname)
        df.to_sql(table_name, conn, index=False, if_exists="replace")
        conn.close()
    else:
        raise ValueError(f"Unsupported export format: .{out_ext}")

    print(f"Data exported to {out_fname}")
    return out_fname

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

def clean_text_column(df, entry):
    """
    entry is a dict with keys:
      - "column":   name of the column
      - "uppercase": string of allowed uppercase chars (e.g. "CFHLMRV")
      - "lowercase": string of allowed lowercase chars (e.g. "al")
      - "numbers":   string of allowed digits (e.g. "0123456789"), or "" to remove all digits
      - "special":   string of allowed special chars (e.g. " ()"), or "" to remove all special chars
    """
    col = entry["column"]
    s = df[col].astype(str)

    print("\ntreating " + col + " \n")
    special = entry.get("special", "")
    if special:
        pattern = f"[^{re.escape(special)}]"
        print("leaving only: " + pattern)
        s = s.str.replace(pattern, "", regex=True)
    else:
        print("removing special characters")
        s = s.str.replace(r"[^A-Za-z0-9\s]+", "", regex=True)

    numbers = entry.get("numbers", "")
    if not numbers:
        print("removing numbers")
        s = s.str.replace(r"\d+", "", regex=True)

    if not entry.get("lowercase"):
        print("converting to uppercase")
        s = s.str.upper()
    if not entry.get("uppercase"):
        print("converting to lowercase")
        s = s.str.lower()

    df[col] = s