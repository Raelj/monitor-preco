"""
Monitor de Preços - Mercado Livre
Coleta o preço de um produto e salva o histórico em CSV.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# ─────────────────────────────────────────
# CONFIGURAÇÕES  (edite aqui)
# ─────────────────────────────────────────
URL_PRODUTO = "https://lista.mercadolivre.com.br/promo%C3%A7%C3%B5es#D[A:promo%C3%A7%C3%B5es]"
ARQUIVO_CSV = "data/historico_precos.csv"
# ─────────────────────────────────────────


def obter_preco(url: str) -> dict | None:
    """
    Acessa a página do produto e extrai o preço atual.
    Retorna um dicionário com data, preço e nome do produto,
    ou None caso não consiga extrair o preço.
    """
    headers = {
        # Simula um navegador real para evitar bloqueio
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Lança erro se status != 200
    except requests.RequestException as e:
        print(f"[ERRO] Não foi possível acessar o site: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Tenta encontrar o preço na página do Mercado Livre
    preco_tag = soup.find("span", class_="andes-money-amount__fraction")
    nome_tag = soup.find("h1", class_="ui-pdp-title")

    if not preco_tag:
        print("[AVISO] Preço não encontrado. O site pode ter mudado sua estrutura.")
        return None

    # Remove pontos de milhar e converte para float
    preco_texto = preco_tag.get_text(strip=True).replace(".", "").replace(",", ".")
    preco = float(preco_texto)
    nome = nome_tag.get_text(strip=True) if nome_tag else "Produto"

    return {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "preco": preco,
        "url": url,
    }


def salvar_historico(dado: dict, arquivo: str) -> None:
    """
    Adiciona uma nova linha ao CSV de histórico.
    Cria o arquivo se não existir.
    """
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    novo_registro = pd.DataFrame([dado])

    if os.path.exists(arquivo):
        historico = pd.read_csv(arquivo)
        historico = pd.concat([historico, novo_registro], ignore_index=True)
    else:
        historico = novo_registro

    historico.to_csv(arquivo, index=False)
    print(f"[OK] Histórico salvo em '{arquivo}'.")


def carregar_historico(arquivo: str) -> pd.DataFrame | None:
    """
    Carrega o CSV de histórico.
    Retorna None se o arquivo não existir ou estiver vazio.
    """
    if not os.path.exists(arquivo):
        print("[INFO] Nenhum histórico encontrado ainda.")
        return None

    df = pd.read_csv(arquivo)
    if df.empty:
        return None

    df["data_hora"] = pd.to_datetime(df["data_hora"])
    return df


def coletar_e_salvar() -> None:
    """
    Função principal: coleta o preço atual e salva no histórico.
    """
    print(f"\n{'='*50}")
    print(f"  Coletando preço em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*50}")

    dado = obter_preco(URL_PRODUTO)

    if dado:
        print(f"  Produto : {dado['nome'][:60]}...")
        print(f"  Preço   : R$ {dado['preco']:,.2f}")
        salvar_historico(dado, ARQUIVO_CSV)
    else:
        print("[ERRO] Coleta falhou. Nenhum dado salvo.")


if __name__ == "__main__":
    coletar_e_salvar()
