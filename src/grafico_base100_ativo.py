"""
Ativo total em índice base 100 (referência = menor trimestre da amostra): Banco Master vs média dos peers.
Lê os CSV em data/extracao_*.csv e exibe o gráfico.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

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
    df["Ativo Total"] = pd.to_numeric(df["Ativo Total"], errors="coerce")
    return df.sort_values(["Instituicao", "Trimestre"])


def format_trimestre(t: int) -> str:
    s = str(int(t))
    ano, mes = s[:4], s[4:]
    q = {"03": "1", "06": "2", "09": "3", "12": "4"}.get(mes, "?")
    return f"{q}T{ano[-2:]}"


def main() -> None:
    df = carregar_consolidado()

    trimestre_ref = int(df["Trimestre"].min())
    ativo_ref = (
        df[df["Trimestre"] == trimestre_ref][["Instituicao", "Ativo Total"]]
        .rename(columns={"Ativo Total": "Ativo_ref"})
    )
    df = df.merge(ativo_ref, on="Instituicao", how="inner")
    df["Base100"] = 100.0 * df["Ativo Total"] / df["Ativo_ref"]

    df_master = df[df["Instituicao"] == MASTER].sort_values("Trimestre")
    df_peers_mean = (
        df[df["Instituicao"] != MASTER]
        .groupby("Trimestre", as_index=False)["Base100"]
        .mean()
        .rename(columns={"Base100": "Media_peers_Base100"})
    )

    trimestres = sorted(set(df_master["Trimestre"]) & set(df_peers_mean["Trimestre"]))
    df_master = df_master[df_master["Trimestre"].isin(trimestres)]
    df_peers_mean = df_peers_mean[df_peers_mean["Trimestre"].isin(trimestres)].sort_values("Trimestre")

    x_labels = [format_trimestre(t) for t in df_master["Trimestre"]]

    plt.figure(figsize=(10, 5))
    plt.plot(
        x_labels,
        df_master["Base100"],
        marker="o",
        linewidth=2,
        color="darkred",
        label="Banco Master",
    )
    plt.plot(
        x_labels,
        df_peers_mean["Media_peers_Base100"],
        marker="s",
        linewidth=2,
        color="gray",
        alpha=0.85,
        label="Média dos peers",
    )
    plt.axhline(100, color="gray", linestyle="--", linewidth=1, alpha=0.7)
    plt.title(
        f"Ativo total — base 100 (ref. {format_trimestre(trimestre_ref)} = 100): Master vs média dos peers",
        fontsize=14,
        fontweight="bold",
    )
    plt.ylabel("Índice (%)", fontsize=12)
    plt.xlabel("Trimestre", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()

    out_dir = Path(__file__).resolve().parent.parent / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir / "grafico_base100_ativo.png", dpi=150, bbox_inches="tight")
    if plt.get_backend().lower() != "agg":
        plt.show()


if __name__ == "__main__":
    main()
