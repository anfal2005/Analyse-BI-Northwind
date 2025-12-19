import pandas as pd
import os

# -----------------------------
# 1. Load both Excel files
# -----------------------------
access_file = r"..\\accessfiles\\Customers (1).xlsx"
sql_file    = r"..\\sqlfiles\\Customers.xlsx"

df_access = pd.read_excel(access_file)
df_sql    = pd.read_excel(sql_file)

# -----------------------------
# 2. Normalize column names
# -----------------------------
def normalize(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

df_access = normalize(df_access)
df_sql = normalize(df_sql)

# -----------------------------
# 3. Clean SQL data
# -----------------------------
sql_map = {
    'customerid': 'customerid',
    'contactname': 'fullname',
    'address': 'address',
    'country': 'country',
    'companyname': 'company'
}

existing_sql_cols = [col for col in sql_map.keys() if col in df_sql.columns]
df_sql_clean = df_sql[existing_sql_cols].rename(columns={k: sql_map[k] for k in existing_sql_cols})

# Fill missing final columns
for col in ['customerid', 'fullname', 'address', 'country', 'company']:
    if col not in df_sql_clean.columns:
        df_sql_clean[col] = ""

# -----------------------------
# 4. Clean Access data
# -----------------------------
access_map = {
    'id': 'customerid',
    'first_name': 'firstname',
    'last_name': 'lastname',
    'address': 'address',
    'country/region': 'country',
    'company': 'company'
}

existing_access_cols = [col for col in access_map.keys() if col in df_access.columns]
df_access_temp = df_access[existing_access_cols].rename(columns={k: access_map[k] for k in existing_access_cols})

# Combine firstname + lastname into fullname
df_access_temp['fullname'] = df_access_temp['firstname'].fillna('') + ' ' + df_access_temp['lastname'].fillna('')
df_access_clean = df_access_temp[['customerid', 'fullname', 'address', 'country', 'company']]

# -----------------------------
# 5. Merge both tables
# -----------------------------
df_customers = pd.concat([df_access_clean, df_sql_clean], ignore_index=True)
df_customers = df_customers.drop_duplicates(subset=['customerid'], keep='first')

# -----------------------------
# 6. Save final merged Excel file
# -----------------------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop, "dbo.client.xlsx")
df_customers.to_excel(output_file, index=False)