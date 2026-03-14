"""
Envia um e-mail de alerta quando o preço cair abaixo do limite definido.

CONFIGURAÇÃO:
  1. Ative a verificação em duas etapas na sua conta Google.
  2. Gere uma "Senha de app" em: https://myaccount.google.com/apppasswords
  3. Preencha as variáveis abaixo.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os

# ─────────────────────────────────────────
# CONFIGURAÇÕES  (edite aqui)
# ─────────────────────────────────────────
EMAIL_REMETENTE = "seu_email@gmail.com"  # Seu e-mail (deve ser o mesmo da senha de app)   
SENHA_APP = "sua_senha_de_app"       # Senha de app do Google (não a senha normal)
EMAIL_DESTINATARIO = "seu_email@gmail.com"  # E-mail que receberá o alerta (pode ser o mesmo do remetente)
PRECO_ALVO = 1500.00                 # Envia alerta quando preço <= este valor
ARQUIVO_CSV = "data/historico_precos.csv"
# ─────────────────────────────────────────


def verificar_e_alertar() -> None:
    """
    Lê o último preço registrado e envia alerta se estiver abaixo do limite.
    """
    if not os.path.exists(ARQUIVO_CSV):
        print("[INFO] Nenhum histórico encontrado. Execute o scraper.py primeiro.")
        return

    df = pd.read_csv(ARQUIVO_CSV)
    if df.empty:
        return

    ultimo = df.iloc[-1]
    preco_atual = ultimo["preco"]
    nome_produto = ultimo["nome"]
    url_produto = ultimo["url"]

    print(f"[INFO] Preço atual: R$ {preco_atual:,.2f} | Alvo: R$ {PRECO_ALVO:,.2f}")

    if preco_atual <= PRECO_ALVO:
        print("[ALERTA] Preço atingiu o alvo! Enviando e-mail...")
        enviar_email(nome_produto, preco_atual, url_produto)
    else:
        print("[OK] Preço ainda acima do alvo. Nenhum alerta enviado.")


def enviar_email(nome: str, preco: float, url: str) -> None:
    """
    Envia um e-mail de alerta com os detalhes do produto.
    """
    assunto = f"🔔 Alerta de Preço: R$ {preco:,.2f}"

    corpo_html = f"""
    <html><body>
    <h2 style="color:#1a73e8;">🛒 Alerta de Queda de Preço!</h2>
    <p>O produto que você está monitorando atingiu o preço alvo.</p>
    <table style="border-collapse:collapse;width:100%">
      <tr><td style="padding:8px;font-weight:bold;">Produto</td>
          <td style="padding:8px;">{nome}</td></tr>
      <tr style="background:#f5f5f5">
          <td style="padding:8px;font-weight:bold;">Preço atual</td>
          <td style="padding:8px;color:#34a853;font-size:1.3em;font-weight:bold;">R$ {preco:,.2f}</td></tr>
      <tr><td style="padding:8px;font-weight:bold;">Seu alvo</td>
          <td style="padding:8px;">R$ {PRECO_ALVO:,.2f}</td></tr>
    </table>
    <br>
    <a href="{url}" style="background:#1a73e8;color:white;padding:10px 20px;
       text-decoration:none;border-radius:5px;">Ver produto →</a>
    <br><br>
    <small style="color:#888;">Monitor de Preços - Projeto Python</small>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO
    msg.attach(MIMEText(corpo_html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMETENTE, SENHA_APP)
            servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        print("[OK] E-mail enviado com sucesso!")
    except smtplib.SMTPAuthenticationError:
        print("[ERRO] Autenticação falhou. Verifique e-mail e senha de app.")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail: {e}")


if __name__ == "__main__":
    verificar_e_alertar()
