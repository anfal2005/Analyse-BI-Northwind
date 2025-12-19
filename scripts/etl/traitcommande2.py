import pandas as pd
import os

# ---------------- FILE PATHS ----------------
access_orders_file = r"..\\accessfiles\\Orders (1).xlsx"
sql_orders_file    = r"..\\sqlfiles\\Orders.xlsx"
access_customers_file = r"..\\accessfiles\\Customers (1).xlsx"
access_employees_file = r"..\\accessfiles\\Employees (1).xlsx"

# ---------------- LOAD FILES ----------------
df_access_orders = pd.read_excel(access_orders_file)
df_sql_orders    = pd.read_excel(sql_orders_file)
df_customers     = pd.read_excel(access_customers_file)
df_employees     = pd.read_excel(access_employees_file)

# ---------------- CLEAN BASIC COLUMN FORMAT ----------------
def normalize(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
        .str.lower()
    )
    return df

df_access_orders = normalize(df_access_orders)
df_sql_orders    = normalize(df_sql_orders)
df_customers     = normalize(df_customers)
df_employees     = normalize(df_employees)

# ---------------- CREATE TEMP IDs FOR ACCESS DIMENSIONS ----------------
df_customers = df_customers.copy()
df_customers["id_client"] = range(1, len(df_customers) + 1)  # sequential IDs
df_customers["company_norm"] = df_customers["company"].str.lower().str.strip()

df_employees = df_employees.copy()
df_employees["id_employee"] = range(1, len(df_employees) + 1)  # sequential IDs
df_employees["full_name"] = df_employees["first_name"].str.strip() + " " + df_employees["last_name"].str.strip()

# ---------------- MAP ACCESS ORDERS TO CUSTOMER IDs BY COMPANY ----------------
df_access_orders["company_norm"] = df_access_orders["customer"].str.lower().str.strip()

# Dictionary: company name -> customer ID
company_to_id = dict(zip(df_customers["company_norm"], df_customers["id_client"]))

# Map Access orders to customer IDs using company name
df_access_orders["customer_id"] = df_access_orders["company_norm"].map(company_to_id)


# ---------------- MAP EMPLOYEE IDs ----------------
df_access_orders["employee_full_name"] = df_access_orders["employee"].str.strip()
df_access_orders = df_access_orders.merge(
    df_employees[["id_employee", "full_name"]],
    left_on="employee_full_name",
    right_on="full_name",
    how="left"
).rename(columns={"id_employee": "employee_id"})

# ---------------- SELECT FINAL ACCESS ORDERS COLUMNS ----------------
df_access_clean = df_access_orders[[
    "order_id", "customer_id", "employee_id", "ship_address", "ship_country_region", "status_id"
]].copy()

# Rename columns to match SQL
df_access_clean = df_access_clean.rename(columns={"ship_country_region": "ship_country"})
df_access_clean["order_status"] = df_access_clean["status_id"].apply(lambda x: 1 if x == 1 else 0)
df_access_clean = df_access_clean.drop(columns=["status_id"])

# ---------------- CLEAN SQL ORDERS ----------------
sql_map = {
    "orderid": "order_id",
    "customerid": "customer_id",
    "employeeid": "employee_id",
    "shipaddress": "ship_address",
    "shipcountry": "ship_country"
}

df_sql_clean = df_sql_orders[list(sql_map.keys())].copy()
df_sql_clean.columns = list(sql_map.values())

# Convert status: delivered if shippeddate exists
df_sql_clean["order_status"] = df_sql_orders["shippeddate"].apply(lambda x: 1 if pd.notna(x) else 0)

# Increment SQL employee IDs by 9
df_sql_clean["employee_id"] = df_sql_clean["employee_id"] + 9

# ---------------- MERGE ACCESS + SQL ----------------
merged = pd.concat([df_access_clean, df_sql_clean], ignore_index=True)
merged = merged.drop_duplicates()

# ---------------- EXPORT TO DESKTOP ----------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop, "dbo.faitcommande2.xlsx")
merged.to_excel(output_file, index=False)

print("Clean merged Orders file created with IDs and status as 1/0!")
print("Saved as:", output_file)
