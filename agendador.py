"""
Agendador: executa o scraper automaticamente a cada intervalo definido.
Execute este arquivo e deixe rodando em segundo plano.

  python agendador.py
"""

import schedule
import time
from scraper import coletar_e_salvar
from grafico import gerar_grafico
from alertas import verificar_e_alertar

# ─────────────────────────────────────────
# CONFIGURAÇÕES
# ─────────────────────────────────────────
INTERVALO_HORAS = 6          # Coleta a cada 6 horas
ARQUIVO_CSV = "data/historico_precos.csv"
ARQUIVO_GRAFICO = "outputs/historico_precos.png"
# ─────────────────────────────────────────


def executar_ciclo() -> None:
    """
    Roda um ciclo completo: coleta → gráfico → alerta.
    """
    coletar_e_salvar()
    gerar_grafico(ARQUIVO_CSV, ARQUIVO_GRAFICO)
    verificar_e_alertar()


def main():
    print(f"🕷️  Monitor de Preços iniciado!")
    print(f"   Coleta agendada a cada {INTERVALO_HORAS} hora(s).")
    print(f"   Pressione Ctrl+C para encerrar.\n")

    # Executa imediatamente na primeira vez
    executar_ciclo()

    # Agenda para repetir
    schedule.every(INTERVALO_HORAS).hours.do(executar_ciclo)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Verifica a cada minuto


if __name__ == "__main__":
    main()
