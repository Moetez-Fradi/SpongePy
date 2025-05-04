# The core logic
import pandas as pd
import numpy as np
import re
from .config_loader import use_config, create_config
from .utils import primary_cleaning

def show_general_stats(df, exp):
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

            strategy = "None"
            message = ""
            if missing_percent > 55:
                message = f"\033[31m    To be deleted\033[0m"
                strategy = "delete"
            elif missing_percent < 5 :
                if df[col].dtype.kind in {"i", "u", "f"}:
                    strategy = "mean"
                    message = f"\033[33m    Replace missing data with mean\033[0m"

            missing_data.append((col, missing_percent, strategy))

            print(f" - \033[1m{col}\033[0m: \033[95m{df[col].isnull().sum():,}\033[0m missing "
      f"(\033[95m{missing_percent:.1f}%\033[0m)" + message)

    else:
        print("\033[1;32mNo columns with missing values found!\033[0m")

    missing_data.sort(key=lambda x: x[1], reverse=True)
    first = True
    second = True
    columns = []
    strColumns = []
    intColumns = []
    potentialCategorical = []
    for col in df.columns:
        columns.append(col)
        if df[col].dtype.kind in {"O", "S", "U"}:
            if exp:
                if first:
                    first = False
                    print_section("STRING COLUMNS ANALYSIS", "🔤")
                print(f"\n\033[1mColumn: {col}\033[0m")

            unique_chars = set()
            for s in df[col].dropna():
                if isinstance(s, (bytes, bytearray)):
                    text = s.decode("utf-8", errors="ignore")
                else:
                    text = str(s)
                unique_chars.update(text)

            su = ''.join(sorted([c for c in unique_chars if c.isupper()]))
            sl = ''.join(sorted([c for c in unique_chars if c.islower()]))
            sn = ''.join(sorted([c for c in unique_chars if c.isdigit()]))
            so = ''.join(sorted([c for c in unique_chars if not c.isalnum()]))

            strColumns.append((col, su, sl, sn, so))

            if exp:
                print(f"  Uppercase: \033[35m{su or 'None'}\033[0m")
                print(f"  Lowercase: \033[35m{sl or 'None'}\033[0m")
                if sn:
                    print(f"  Numbers:   \033[35m{sn or 'None'}\033[0m")
                if so:
                    print(f"  Special:   \033[35m{so or 'None'}\033[0m")
        
        if df[col].dtype.kind in {"i", "u", "f"}:
            intColumns.append((col, df[col].min(), df[col].mean(), df[col].max()))
    
        if df[col].nunique() < 10:
            potentialCategorical.append((col, df[col].nunique()))

    if exp:
        print_section(" NUMERICAL COLUMNS ANALYSIS", "#️⃣")
        for col, mino, mean, maxo in intColumns:
            print(f"\n\033[1mColumn: {col}\033[0m")
            print(f"  max: \033[35m{maxo or 'NaN'}\033[0m")
            print(f"  mean: \033[35m{mean or 'NaN'}\033[0m")
            print(f"  min:   \033[35m{mino or 'NaN'}\033[0m")

    missing_data.sort(key=lambda x: x[2], reverse=True)
    create_config({
        "columns":     columns,
        "missing-data": missing_data,
        "text-columns" : strColumns,
        "numeric-columns" : intColumns,
        "potential-categorical" : potentialCategorical
    })

def configured_cleaning(df, config):
    print("importing configuration")
    cfg = use_config(config)

    missing_data = cfg["missing-data"]

    for col, _, strategy in missing_data:
        if strategy == "None":
            continue
        elif strategy == "mean":
            mean_val = df[col].mean()
            df[col].fillna(mean_val, inplace=True)
        elif strategy == "medium":
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
        elif strategy == "delete":
            df.dropna(subset=[col], inplace=True)

    phone_number = cfg.get("phone-number")
    if phone_number:
        if isinstance(phone_number, str):
            fix_phone_number(df, phone_number)
        elif isinstance(phone_number, list):
            for col in phone_number:
                fix_phone_number(df, col)

    name = cfg.get("name")
    if name:
        if isinstance(name, str):
            fix_name(df, name)
        elif isinstance(name, list):
            for col in name:
                fix_name(df, col)

    broken_id = cfg.get("broken-id")
    if broken_id:
        if isinstance(broken_id, str):
            construct_id_column(df, broken_id)
        elif isinstance(broken_id, list):
            for col in broken_id:
                construct_id_column(df, col)

    id = cfg.get("id")
    if id:
        if isinstance(id, str):
            fix_id_column(df, id)
        elif isinstance(id, list):
            for col in id:
                fix_id_column(df, col)


def default_cleaning(df):
    primary_cleaning(df)
    fill_missing_data(df)
    fix_id_column(df, "id")