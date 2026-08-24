import pandas as pd
import numpy as np
from .config import RAW_DIR, PROCESSED_DIR

def carregar_ideb() -> pd.DataFrame:
    df = pd.read_excel(RAW_DIR / "ideb_municipios.xlsx",skiprows=9,na_values=["-","**","*"])
    return df

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip().str.lower().str.normalize("NFKD").str.encode("ascii",errors="ignore").str.decode("ascii")
        .str.replace(r"\s+","_", regex=True).str.replace(r"[^\w]","", regex=True)
    )
    return df
def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ideb_2023"] = pd.to_numeric(df["ideb_2023"], errors="coerce")
    df["uf"] = df["uf"].astype("category")
    return df
def remover_outliers_iqr(df:pd.DataFrame, coluna:str, k:float = 1.5) -> pd.DataFrame:
    q1, q3 = df[coluna].quantile([0.25,0.75])
    iqr = q3 - q1
    return df[df[coluna].between(q1 - (k * iqr), q3 + (k * iqr))]

def limpar(df: pd.DataFrame) -> pd.DataFrame:
    return(df.pipe(padronizar_colunas).pipe(converter_tipos).dropna(subset=["ideb_2023","uf"]).drop_duplicates())

def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = carregar_ideb().pipe(limpar)
    df.ti_parquet(PROCESSED_DIR / "ideb_municipios.parquet")
    print(f"[ok] {len(df):,} municipios após limpeza")

if __name__ == "__main__":
    main()