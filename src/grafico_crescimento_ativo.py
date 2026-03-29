"""
Trajetória de crescimento do ativo (%): Banco Master vs média dos peers.
Lê os CSV em data/extracao_*.csv e exibe o gráfico (com tendências por regressão linear).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

MASTER = "Banco Master"
DATA_GLOB = "extracao_*.csv"


def _data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


def carregar_consolidado() -> pd.DataFrame:
    paths = sorted(_data_dir().glob(DATA_GLOB))
    if not paths:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {_data_dir()} com padrão {DATA_GLOB}")
    frames = [pd.read_csv(p) for p in paths]
    df = pd.concat(frames, ignore_index=True)
    df["Trimestre"] = df["Trimestre"].astype(int)
    for col in ("Asset Growth (%)",):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values(["Instituicao", "Trimestre"])


def format_trimestre(t: int) -> str:
    s = str(int(t))
    ano, mes = s[:4], s[4:]
    q = {"03": "1", "06": "2", "09": "3", "12": "4"}.get(mes, "?")
    return f"{q}T{ano[-2:]}"


def calcular_tendencia(y_values: np.ndarray) -> np.ndarray:
    x = np.arange(len(y_values)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y_values)
    return model.predict(x)


def main() -> None:
    df = carregar_consolidado()

    df_master = df[df["Instituicao"] == MASTER].copy()
    df_market = (
        df[df["Instituicao"] != MASTER]
        .groupby("Trimestre", as_index=False)["Asset Growth (%)"].mean()
        .rename(columns={"Asset Growth (%)": "Market_Avg_Asset_Growth"})
    )

    df_master = df_master.dropna(subset=["Asset Growth (%)"])
    df_market = df_market.dropna(subset=["Market_Avg_Asset_Growth"])

    trimestres = sorted(set(df_master["Trimestre"]) & set(df_market["Trimestre"]))
    df_master = df_master[df_master["Trimestre"].isin(trimestres)].sort_values("Trimestre")
    df_market = df_market[df_market["Trimestre"].isin(trimestres)].sort_values("Trimestre")

    x_labels = [format_trimestre(t) for t in df_master["Trimestre"]]
    y_m = df_master["Asset Growth (%)"].values
    y_mk = df_market["Market_Avg_Asset_Growth"].values

    trend_master = calcular_tendencia(y_m)
    trend_market = calcular_tendencia(y_mk)

    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, y_m, marker="s", color="orange", linewidth=2, label="Banco Master (real)")
    plt.plot(
        x_labels,
        y_mk,
        marker="o",
        color="gray",
        linewidth=2,
        alpha=0.7,
        label="Média dos peers (real)",
    )
    plt.plot(x_labels, trend_master, "--", color="darkorange", linewidth=1.5, label="Tendência Banco Master")
    plt.plot(
        x_labels,
        trend_market,
        "--",
        color="black",
        linewidth=1.5,
        alpha=0.6,
        label="Tendência média peers",
    )

    plt.title("Banco Master vs média dos peers: crescimento do ativo (%)", fontsize=14, fontweight="bold", pad=20)
    plt.xlabel("Trimestre", fontsize=12)
    plt.ylabel("Crescimento do ativo (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()

    out_dir = Path(__file__).resolve().parent.parent / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir / "grafico_crescimento_ativo.png", dpi=150, bbox_inches="tight")
    if plt.get_backend().lower() != "agg":
        plt.show()


if __name__ == "__main__":
    main()
