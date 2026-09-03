import pandas as pd
import numpy as np
from .config import PROCESSED_DIR

def carregar_limpo() -> pd.DataFrame:
    return pd.read_parquet(PROCESSED_DIR/"ideb_brasil_anos_finais.parquet")

def sumario_por_regiao(df:pd.DataFrame) -> pd.DataFrame:
    mapa_regiao ={
    "SP": "Sudeste", "RJ": "Sudeste", "ES": "Sudeste", "MG": "Sudeste",
    "PR": "Sul","RS": "Sul", "SC": "Sul",
    "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste", "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste","TO": "Nordeste",
    "AM": "Norte", "AP": "Norte", "PA": "Norte", "RO": "Norte", "RR": "Norte", "AL":"Norte",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste", "MS": "Centro-Oeste",
    }
    df = df.assign(regiao = df["UF"].map(mapa_regiao))
    return df.groupby("regiao").agg(
        n=("IDEB", "count"),
        media=("IDEB", "mean"),
        mediana=("IDEB", "median"),
        desvio=("IDEB", "std"),
        minimo=("IDEB", "min"),
        maximo=("IDEB", "max"),
    ).sort_values(by="media", ascending=False)

def matriz_correlacao(df:pd.DataFrame, colunas_numericas:list[str]) -> pd.DataFrame:
    return df[colunas_numericas].corr(method="pearson")

def top_bottom_n(df:pd.DataFrame, coluna:str, n:int = 10) -> tuple[pd.DataFrame, pd.DataFrame]:
    ordenado = df.sort_values(by=coluna, ascending=False)
    return ordenado.head(n), ordenado.tail(n)
        
