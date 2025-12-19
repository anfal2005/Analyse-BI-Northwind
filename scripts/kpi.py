import pandas as pd

# -----------------------------
# Fonctions KPI
# -----------------------------

def add_flags(df):
    """
    Ajoute les colonnes :
    - delivered
    - not_delivered
    - year
    - month
    - year_month
    """
    df = df.copy()

    # flags livraison
    df['delivered'] = df['order_status'] == 1
    df['not_delivered'] = df['order_status'] == 0

    # colonne date (dimension temps)
    df['startdate'] = pd.to_datetime(df['startdate'])

    # année / mois
    df['year'] = df['startdate'].dt.year
    df['month'] = df['startdate'].dt.month

    # format BI : YYYY-MM
    df['year_month'] = (
        df['year'].astype(str) + '-' +
        df['month'].astype(str).str.zfill(2)
    )

    return df


# -----------------------------
# KPI globaux
# -----------------------------

def kpi_total_delivered(df_filtered):
    return int(df_filtered['delivered'].sum())


def kpi_total_not_delivered(df_filtered):
    return int(df_filtered['not_delivered'].sum())


# -----------------------------
# KPI par dimension
# -----------------------------

def kpi_by_employee(df_filtered):
    return (
        df_filtered
        .groupby('employee_name')
        .agg(
            Delivered=('delivered', 'sum'),
            Not_Delivered=('not_delivered', 'sum')
        )
        .reset_index()
        .sort_values('Delivered', ascending=False)
    )


def kpi_by_client(df_filtered):
    return (
        df_filtered
        .groupby('client_name')
        .agg(
            Delivered=('delivered', 'sum'),
            Not_Delivered=('not_delivered', 'sum')
        )
        .reset_index()
        .sort_values('Delivered', ascending=False)
    )


def kpi_by_year_month(df_filtered):
    return (
        df_filtered
        .groupby('year_month')
        .agg(
            Delivered=('delivered', 'sum'),
            Not_Delivered=('not_delivered', 'sum')
        )
        .reset_index()
        .sort_values('year_month')
    )
