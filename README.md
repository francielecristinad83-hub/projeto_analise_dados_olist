# 📊 Análise de Dados — E-commerce Olist

## Sobre o projeto

Este projeto tem como objetivo analisar dados de um e-commerce brasileiro utilizando Python, buscando identificar padrões de vendas, compreender o desempenho comercial e explorar indicadores relacionados aos pedidos e às entregas.

O trabalho foi desenvolvido como projeto de portfólio para praticar habilidades de análise e visualização de dados.

## 🎯 Objetivos

* Analisar os pedidos e o desempenho das entregas.
* Investigar a evolução mensal do faturamento.
* Identificar os produtos mais vendidos.
* Comparar o faturamento entre categorias de produtos.
* Explorar indicadores comerciais para identificar padrões relevantes.

## 🛠️ Tecnologias utilizadas

* **Python:** linguagem utilizada no desenvolvimento.
* **Pandas:** manipulação, limpeza e análise dos dados.
* **Matplotlib:** criação de gráficos e visualizações.
* **Visual Studio Code:** ambiente de desenvolvimento.

## 📁 Estrutura do projeto

```text
projeto-analise-dados/
├── dados/
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   └── product_category_name_translation.csv
├── analise_vendas.py
└── README.md
```

## 📈 Principais análises

### 1. Pedidos e entregas

Investigação da situação dos pedidos e dos prazos de entrega, incluindo a comparação entre as datas de entrega e as previsões informadas.

### 2. Evolução do faturamento

Análise do faturamento mensal dos itens associados aos pedidos entregues, agrupados pelo mês da compra.

### 3. Produtos mais vendidos

Identificação dos produtos com maior quantidade de unidades vendidas nos pedidos entregues.

### 4. Faturamento por categoria

Comparação da receita dos produtos entre diferentes categorias, permitindo identificar as categorias com maior faturamento.

## 🔎 Alguns resultados encontrados

* Novembro de 2017 apresentou o maior faturamento mensal da série analisada, com **R$ 987.765,37**.
* Nesse mesmo mês, foram registrados **7.289 pedidos entregues** na análise.
* A categoria `beleza_saude` apresentou faturamento de **R$ 1.233.131,72** na análise dos itens entregues.
* A categoria `cama_mesa_banho` apresentou a maior quantidade de unidades vendidas entre as categorias analisadas, com **10.953 unidades**.

Os resultados consideram os filtros e critérios utilizados no projeto. Portanto, representam os dados analisados, e não necessariamente todos os indicadores financeiros ou operacionais da empresa.

## 💡 Aprendizados

Durante o desenvolvimento, foram praticados conceitos importantes de análise de dados:

* Leitura de arquivos CSV com Pandas.
* Seleção, filtragem e organização de dados.
* Junção de tabelas utilizando chaves comuns.
* Agrupamento de informações com `groupby()`.
* Cálculo de somas, médias e contagens.
* Ordenação e comparação de resultados.
* Criação de gráficos com Matplotlib.
* Verificação da consistência dos resultados.

Uma das principais lições do projeto foi a importância de verificar se as junções entre tabelas estão corretas, pois duplicações podem alterar os resultados das análises.

## ▶️ Como executar o projeto

### Pré-requisitos

* Python instalado.
* Bibliotecas Pandas e Matplotlib.

### Instalação das dependências

No terminal, execute:

```bash
pip install pandas matplotlib
```

### Execução

Na pasta principal do projeto, execute:

```bash
python analise_vendas.py
```

Os arquivos CSV necessários devem permanecer na pasta `dados`, respeitando os nomes e caminhos utilizados no código.

## 📌 Considerações finais

Este projeto representa uma aplicação prática de Python para análise exploratória de dados de e-commerce.

O desenvolvimento permitiu trabalhar com dados de pedidos, produtos, categorias e entregas, além de praticar a transformação de dados em informações úteis para apoiar a compreensão do negócio.
