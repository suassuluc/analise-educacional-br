import pandas as pd
import pytest
from src.cleaning import padronizar_colunas, remover_outliers_iqr

def test_padronizar_colunas_remove_acento_e_espaco():
    df = pd.DataFrame(columns=["Nome do Município", "IDEB 2023"])
    resultado = padronizar_colunas(df)
    assert list(resultado.columns) == ["nome_do_municipio","ideb_2023"]
    
def test_remover_outliers_reduz_amostra():
    df = pd.DataFrame({"x":[1, 2, 3, 4, 5, 100]})
    resultado = remover_outliers_iqr(df,"x")
    assert 100 not in resultado["x"].values
    assert len(resultado)  < len(df)