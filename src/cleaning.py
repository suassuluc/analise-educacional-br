import pandas as pd
import numpy as np
from .config import RAW_DIR, PROCESSED_DIR

ABA_ANOS_FINAIS = "Brasil (Anos Finais)"
COLUNA_IDEB = "vl_observado_2025"
COLUNA_REDE = "rede"


def carregar_ideb() -> pd.DataFrame:
    arquivo = RAW_DIR / "divulgacao_brasil_ideb_2025" / "divulgacao_brasil_ideb_2025.xlsx"
    df = pd.read_excel(
        arquivo,
        sheet_name=ABA_ANOS_FINAIS,
        skiprows=9,
        na_values=["-", "**", "*"],
    )
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
    df[COLUNA_IDEB] = pd.to_numeric(df[COLUNA_IDEB], errors="coerce")
    df[COLUNA_REDE] = df[COLUNA_REDE].astype("category")
    return df
def remover_outliers_iqr(df:pd.DataFrame, coluna:str, k:float = 1.5) -> pd.DataFrame:
    q1, q3 = df[coluna].quantile([0.25,0.75])
    iqr = q3 - q1
    return df[df[coluna].between(q1 - (k * iqr), q3 + (k * iqr))]

def limpar(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.pipe(padronizar_colunas)
        .pipe(converter_tipos)
        .dropna(subset=[COLUNA_IDEB, COLUNA_REDE])
        .drop_duplicates()
    )

def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = carregar_ideb().pipe(limpar)
    df.to_parquet(PROCESSED_DIR / "ideb_brasil_anos_finais.parquet")
    print(f"[ok] {len(df):,} linhas após limpeza")

if __name__ == "__main__":
    main()
