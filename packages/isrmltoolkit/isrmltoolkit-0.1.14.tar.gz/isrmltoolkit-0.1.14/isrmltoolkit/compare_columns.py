import pandas as pd
import numpy as np

def check_multicollinearity(X, threshold=0.9):
    """
    Devuelve pares de columnas con correlación absoluta mayor que el umbral dado.

    Parámetros:
    - X: DataFrame numérico (no incluye el target).
    - threshold: valor de corte para considerar alta correlación.

    Retorna:
    - Lista de tuplas: (col1, col2, correlation)
    """
    corr_matrix = X.corr().abs()
    upper = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    corr_pairs = corr_matrix.where(upper).stack()

    high_corr = corr_pairs[corr_pairs > threshold]
    results = [(i, j, corr_pairs[i, j]) for i, j in high_corr.index]

    return sorted(results, key=lambda x: -x[2])
