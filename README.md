# 🕷️ Monitor de Preços

> Scraper Python que acompanha o histórico de preços de produtos no Mercado Livre, gera gráficos automáticos e envia alertas por e-mail quando o preço cai.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-ativo-brightgreen)

---

## 📋 Funcionalidades

- **Coleta automática** de preço via web scraping (BeautifulSoup)
- **Histórico em CSV** com data e hora de cada coleta
- **Gráfico de evolução** do preço ao longo do tempo
- **Alerta por e-mail** quando o preço atinge o valor desejado
- **Agendamento** configurável (padrão: a cada 6 horas)

---

## 🖼️ Exemplo de gráfico gerado

```
R$ 1.800 ┤                         ╭──●
R$ 1.700 ┤           ╭────╮       ╯
R$ 1.600 ┤   ●───╮  ╯     ╰──╮  ╯
R$ 1.500 ┤──╯    ╰──╯         ╰──
         └──────────────────────────
          seg    ter   qua   qui   sex
```

---

## 🗂️ Estrutura do projeto

```
monitor_precos/
├── scraper.py        # Coleta o preço e salva no CSV
├── grafico.py        # Gera o gráfico de histórico
├── alertas.py        # Envia e-mail quando o preço cai
├── agendador.py      # Orquestra tudo automaticamente
├── requirements.txt  # Dependências do projeto
├── data/
│   └── historico_precos.csv   # Gerado automaticamente
└── outputs/
    └── historico_precos.png   # Gerado automaticamente
```

---

## 🚀 Como usar

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configure o produto a monitorar

Abra o `scraper.py` e altere a variável:
```python
URL_PRODUTO = "https://www.mercadolivre.com.br/seu-produto-aqui"
```

### 3. (Opcional) Configure alertas por e-mail

Abra o `alertas.py` e preencha:
```python
EMAIL_REMETENTE    = "seu_email@gmail.com"
SENHA_APP          = "xxxx xxxx xxxx xxxx"  # Senha de app do Google
EMAIL_DESTINATARIO = "seu_email@gmail.com"
PRECO_ALVO         = 1500.00
```

> **Dica:** para gerar a senha de app do Gmail, acesse:
> Conta Google → Segurança → Verificação em duas etapas → Senhas de app

### 4. Execute

**Coleta única:**
```bash
python scraper.py
```

**Gerar gráfico:**
```bash
python grafico.py
```

**Monitoramento contínuo (recomendado):**
```bash
python agendador.py
```

---

## 🛠️ Tecnologias utilizadas

| Biblioteca | Uso |
|---|---|
| `requests` | Requisições HTTP |
| `BeautifulSoup4` | Parsing do HTML |
| `pandas` | Manipulação e armazenamento dos dados |
| `matplotlib` | Geração dos gráficos |
| `schedule` | Agendamento das coletas |
| `smtplib` | Envio de e-mail (nativo Python) |

---

## 📌 Observações

- O scraper funciona com a estrutura atual do Mercado Livre. Mudanças no site podem exigir ajustes nos seletores CSS em `scraper.py`.
- Para monitorar outros sites (Amazon, Kabum, etc.), basta adaptar a função `obter_preco()` com os seletores corretos.

---

## 📄 Licença

© 2026 Raeljoss
