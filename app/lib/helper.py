import pandas as pd

def reader(path):
    ext = path.split(".")[1]
    if ext ==  "csv":
        df = pd.read_csv(path)
    elif ext == "xlsx":
        df = pd.read_excel(path)
    return df

def table_return(df):
    head = df.columns.tolist()
    values = df.values.tolist()
    return head, values

def list_relation(table):
    data = table.query.all()
    fields = {}
    tables = []
    for i in data:
        df = reader(i.pathfile)
        fields[str(i.id)] = df.columns.tolist()
        tables.append({
            "id":i.id,
            "name":i.name
        })
    return fields, tables

def save_to_datastore(df, path):
    ext = path.split(".")[1]
    if ext == "csv":
        df.to_csv(path, index=False)
    else:
        df.to_excel(path, index=False)
    
