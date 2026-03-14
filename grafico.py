"""
Gera um gráfico do histórico de preços salvo no CSV.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

ARQUIVO_CSV = "data/historico_precos.csv"
ARQUIVO_GRAFICO = "outputs/historico_precos.png"


def gerar_grafico(arquivo_csv: str, arquivo_saida: str) -> None:
    """
    Lê o histórico de preços e salva um gráfico em PNG.
    """
    if not os.path.exists(arquivo_csv):
        print("[ERRO] Arquivo CSV não encontrado. Execute o scraper.py primeiro.")
        return

    df = pd.read_csv(arquivo_csv)
    df["data_hora"] = pd.to_datetime(df["data_hora"])

    if df.empty:
        print("[ERRO] O histórico está vazio.")
        return

    nome_produto = df["nome"].iloc[-1][:50]
    preco_min = df["preco"].min()
    preco_max = df["preco"].max()
    preco_atual = df["preco"].iloc[-1]

    # ── Estilo do gráfico ──────────────────────────────────
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 5))

    # Linha principal
    ax.plot(
        df["data_hora"],
        df["preco"],
        color="#1a73e8",
        linewidth=2,
        marker="o",
        markersize=5,
        label="Preço",
    )

    # Área sombreada abaixo da linha
    ax.fill_between(df["data_hora"], df["preco"], alpha=0.1, color="#1a73e8")

    # Linha de preço mínimo (tracejada)
    ax.axhline(
        preco_min,
        color="#34a853",
        linestyle="--",
        linewidth=1.2,
        label=f"Mínimo: R$ {preco_min:,.2f}",
    )

    # ── Formatação dos eixos ────────────────────────────────
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
    plt.xticks(rotation=30, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"R$ {x:,.0f}")
    )

    # ── Títulos e anotações ─────────────────────────────────
    ax.set_title(
        f"Histórico de Preços\n{nome_produto}...",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Data / Hora", fontsize=10)
    ax.set_ylabel("Preço (R$)", fontsize=10)
    ax.legend(fontsize=9)

    # Anotação do preço atual
    ax.annotate(
        f"Atual\nR$ {preco_atual:,.2f}",
        xy=(df["data_hora"].iloc[-1], preco_atual),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=9,
        color="#1a73e8",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#1a73e8", alpha=0.8),
    )

    # ── Salvar ──────────────────────────────────────────────
    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=150)
    plt.close()

    print(f"[OK] Gráfico salvo em '{arquivo_saida}'.")
    print(f"     Mínimo: R$ {preco_min:,.2f} | Máximo: R$ {preco_max:,.2f} | Atual: R$ {preco_atual:,.2f}")


if __name__ == "__main__":
    gerar_grafico(ARQUIVO_CSV, ARQUIVO_GRAFICO)
