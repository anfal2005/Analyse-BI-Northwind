import pandas as pd
import os

#FILE PATHS
access_file = r"..\\accessfiles\\Employees (1).xlsx"
sql_file    = r"..\\sqlfiles\\Employees.xlsx"

# LOAD FILES
df_access = pd.read_excel(access_file)
df_sql = pd.read_excel(sql_file)

#CLEAN BASIC COLUMN FORMAT
def normalize(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.lower()
    )
    return df

df_access = normalize(df_access)
df_sql = normalize(df_sql)

#ATTRIBUTE MAPPING (CLEAN NAME → SOURCE NAME)

# Access column names (updated)
access_map = {
    "employeeid": "id",
    "firstname": "first_name",
    "lastname": "last_name",
    "address": "address",
    "country": "country/region",
    "homenumber": "home_phone",
    "job": "job_title",
    "region": "state/province",
}

# SQL Server column names (updated)
sql_map = {
    "employeeid": "employeeid",
    "firstname": "firstname",
    "lastname": "lastname",
    "address": "address",
    "country": "country",
    "homenumber": "homephone",
    "job": "title",
    "region": "region",
}

#SELECT & RENAME COLUMNS

df_access_clean = df_access[[access_map[k] for k in access_map.keys()]]
df_access_clean.columns = access_map.keys()

df_sql_clean = df_sql[[sql_map[k] for k in sql_map.keys()]]
df_sql_clean.columns = sql_map.keys()

df_sql_clean = df_sql_clean.copy()
df_sql_clean['employeeid'] = range(10, 10 + len(df_sql_clean))

#MERGE BOTH

merged = pd.concat([df_access_clean, df_sql_clean], ignore_index=True)

# Remove duplicates
merged = merged.drop_duplicates()

#EXPORT TO DESKTOP
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop, "dbo.employee.xlsx")

merged.to_excel(output_file, index=False)

print("Clean merged Employees file created!")