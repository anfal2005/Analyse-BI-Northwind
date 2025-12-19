import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from kpi import (
    add_flags,
    kpi_total_delivered,
    kpi_total_not_delivered,
    kpi_by_employee,
    kpi_by_client,
    kpi_by_year_month
)

st.set_page_config(page_title="KPI Dashboard", layout="wide")

# -----------------------------
# 1️⃣ Connexion SQL Server
# -----------------------------
conn_str = "mssql+pyodbc://DESKTOP-VT8AV69\\SQLEXPRESS/DataWarehouse?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn_str)

# -----------------------------
# 2️⃣ Charger les données
# -----------------------------
@st.cache_data
def load_data():
    df_fact = pd.read_sql("SELECT * FROM faitcommande", engine)
    df_client = pd.read_sql("SELECT id_client, fullname AS client_name FROM client", engine)
    df_employee = pd.read_sql("SELECT id_employee, firstname+' '+lastname AS employee_name FROM employee", engine)
    df_temps = pd.read_sql("SELECT id_date, startdate FROM temps", engine)

    df = (
        df_fact
        .merge(df_client, left_on='customer_id', right_on='id_client', how='left')
        .merge(df_employee, left_on='employee_id', right_on='id_employee', how='left')
        .merge(df_temps, left_on='date_id', right_on='id_date', how='left')
    )

    return add_flags(df)

df = load_data()

# -----------------------------
# 3️⃣ Dashboard
# -----------------------------
st.title("📊 KPI Dashboard - Orders")

# ---------- Filtres ----------
col1, col2, col3 = st.columns(3)

with col1:
    employee_filter = st.selectbox(
        "Employee",
        ["All"] + sorted(df['employee_name'].dropna().unique().tolist())
    )

with col2:
    client_filter = st.selectbox(
        "Client",
        ["All"] + sorted(df['client_name'].dropna().unique().tolist())
    )

with col3:
    min_date = df['startdate'].min()
    max_date = df['startdate'].max()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date)
    )

# -----------------------------
# 4️⃣ Appliquer les filtres
# -----------------------------
filtered = df.copy()

if employee_filter != "All":
    filtered = filtered[filtered['employee_name'] == employee_filter]

if client_filter != "All":
    filtered = filtered[filtered['client_name'] == client_filter]

# sécuriser date_input
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered = filtered[
        (filtered['startdate'] >= start_date) &
        (filtered['startdate'] <= end_date)
    ]

# -----------------------------
# 5️⃣ KPIs globaux
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "✅ Delivered Orders",
        kpi_total_delivered(filtered)
    )

with col2:
    st.metric(
        "❌ Not Delivered Orders",
        kpi_total_not_delivered(filtered)
    )

# -----------------------------
# 6️⃣ KPI par temps
# -----------------------------
st.subheader("📅 KPI by Month")

kpi_time = kpi_by_year_month(filtered)

st.dataframe(kpi_time, use_container_width=True)

st.line_chart(
    kpi_time.set_index('year_month')[['Delivered', 'Not_Delivered']]
)

# -----------------------------
# 7️⃣ KPI par employé
# -----------------------------
st.subheader("👨‍💼 KPI by Employee")

kpi_emp = kpi_by_employee(filtered)

st.dataframe(kpi_emp, use_container_width=True)
st.line_chart(
    kpi_emp.set_index('employee_name')[['Delivered', 'Not_Delivered']]
)

# -----------------------------
# 8️⃣ KPI par client
# -----------------------------
st.subheader("👤 KPI by Client")

kpi_cli = kpi_by_client(filtered)

st.dataframe(kpi_cli, use_container_width=True)
st.bar_chart(
    kpi_cli.set_index('client_name')[['Delivered', 'Not_Delivered']]
)
