import pandas as pd

def rename_col(df:pd.DataFrame(), column:str, rename_to:str):
    df.rename(columns={column:rename_to}, inplace=True)
    return df

def del_column(df:pd.DataFrame(), column:str):
    df.drop(column, axis=1, inplace=True)
    return df

def select_column(df:pd.DataFrame(), cols:list):
    df = df[cols]
    return df

def filter_str(df:pd.DataFrame(), column:str, pattern:str, method:str="contains"):
    if method == "contains":
        df = df[(df[column].notna())&(df[column].str.contains(pattern))]
    elif method == "startswith":
        df = df[(df[column].notna())&(df[column].str.startswith(pattern))]
    else:
        df = df[(df[column].notna())&(df[column].str.endswith(pattern))]
    return df

def replace_str(df:pd.DataFrame(), col:str, pat:str, repl:str):
    df[col] = df[col].str.replace(pat, repl, regex=False)
    return df

def filter(df:pd.DataFrame(), col:str, max:float=None, min:float=None):
    if max and min:
        df = df[(df[col]>=min)&(df[col]<=max)]
    elif max:
        df = df[df[col]<=max]
    elif min:
        df = df[df[col]>=min]
    return df

def join(left_table:pd.DataFrame(),left_key:str, right_table:pd.DataFrame(), 
        right_key:str, method:str="inner"):
    df = left_table.merge(right_table, how=method, 
                    left_on=left_key, right_on=right_key)
    return df