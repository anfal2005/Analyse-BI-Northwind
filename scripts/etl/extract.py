import pyodbc
import pandas as pd
import os

#PATH TO DESKTOP
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
#CONNECTION
server = r'DESKTOP-VT8AV69\SQLEXPRESS'
database = 'Northwind'

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# GET ALL TABLES 
cursor.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE'
""")
tables = [row[0] for row in cursor.fetchall()]

#EXPORT EACH TABLE
for table in tables:
    print(f"Exporting: {table} ...")
    df = pd.read_sql(f"SELECT * FROM [{table}]", conn)
    file_path = os.path.join(desktop, f"{table}.xlsx")
    df.to_excel(file_path, index=False)