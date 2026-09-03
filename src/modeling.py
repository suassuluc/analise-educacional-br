
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from .config import SEED


def clusteriza_redes(df:pd.DataFrame, features:list[str], k: int = 3) -> pd.DataFrame: 
    x = df[features].values
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("km", KMeans(n_clusters=k, random_state=SEED, n_init=10)),
    ])
    pipe.fit(x)
    df = df.copy()
    df["cluster"] = pipe.named_steps["km"].labels_
    return df

def regressao_baseline(df:pd.DataFrame, x_cols:list[str], y_col:str) -> dict:
    X = df[x_cols].values
    y = df[y_col].values
    modelo = LinearRegression().fit(X, y)
    y_pred = modelo.predict(X)
    return {
        "r2": r2_score(y, y_pred),
        "mae": mean_absolute_error(y, y_pred),
        "coeficiente": modelo.coef_,
        "intercepto": modelo.intercept_,
    }