import pandas as pd

def auto_detect_datetime_columns(df):
    """
    Detecta columnas que parecen contener fechas y las convierte a tipo datetime.

    Parámetros:
    - df: DataFrame original

    Retorna:
    - DataFrame con columnas convertidas (si aplica)
    - Lista de columnas que fueron convertidas
    """
    converted_cols = []
    df_copy = df.copy()
    
    for col in df_copy.columns:
        if df_copy[col].dtype == 'object' or df_copy[col].dtype.name == 'string':
            try:
                converted = pd.to_datetime(df_copy[col], errors='raise')
                df_copy[col] = converted
                converted_cols.append(col)
            except (ValueError, TypeError):
                continue

    return df_copy, converted_cols
