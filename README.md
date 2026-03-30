## Interface para visualização

A interface interativa com os gráficos e as interpretações financeiras está publicada e pode ser acessada aqui:

**[analisemaster.netlify.app](https://analisemaster.netlify.app/)**

# Análise de Indicadores Financeiros: Banco Master vs Peers

Este repositório contém o código-fonte da interface web e os scripts de extração de dados desenvolvidos para a análise comparativa do balanço do Banco Master em relação à média de seus pares no mercado. 

O foco do estudo é avaliar o ritmo de expansão do balanço e o uso de capital de terceiros (alavancagem) ao longo dos últimos trimestres, estruturado como parte do escopo de projetos analíticos do IBMEC.

## ⚙️ Arquitetura e Fluxo de Dados

O projeto é dividido em duas frentes principais:

1. **Engenharia de Dados (Python):** * Scripts desenvolvidos para consumir a API pública do **IF.data (Banco Central do Brasil)**.
   * Tratamento das séries temporais financeiras e cálculo das métricas de interesse (Asset Growth, Base 100, Alavancagem PL).
   * Exportação dos dados consolidados em formato CSV.
2. **Apresentação (Frontend):** * Interface estática e responsiva, sem dependências de frameworks pesados.
   * Navegação estruturada em abas (tabs) para segmentar a análise de cada indicador.

## 🛠️ Tecnologias Utilizadas

* **Dados:** Python
* **Frontend:** HTML5, CSS3, JavaScript puro

## 📂 Estrutura de Diretórios

* `/data/` — Arquivos `.csv` com o histórico trimestral das instituições.
* `/figures/` — Gráficos exportados da análise em Python (`.png`).
* `index.html` — Estrutura semântica e textos de interpretação do dashboard.
* `styles.css` — Estilização da página e componentes.
* `tabs.js` — Lógica de controle de estado das abas de navegação.
