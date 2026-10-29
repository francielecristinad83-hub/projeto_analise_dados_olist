import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dados/olist_orders_dataset.csv")
clientes = pd.read_csv("dados/olist_customers_dataset.csv")

print("\n--- DADOS DOS CLIENTES ---")
print(clientes.head())

print("\nColunas disponíveis:")
print(clientes.columns.tolist())

print("\nDimensões da tabela:")
print(df.shape)

print("\nNomes das colunas:")
print(df.columns.tolist())

print("\nInformações da tabela:")
df.info()

print("\nValores ausentes por coluna:")
print(df.isnull().sum())


print("\nQuantidade de pedidos por status:")
print(df["order_status"].value_counts())

print("\nValores ausentes por status do pedido:")
print(df.groupby("order_status")[
    [
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date"
    ]
].apply(lambda grupo: grupo.isnull().sum()))


# Calcular a quantidade total de pedidos
total_pedidos = len(df)

# Contar os pedidos entregues
pedidos_entregues = (df["order_status"] == "delivered").sum()

# Calcular a porcentagem de pedidos entregues
porcentagem_entregues = (pedidos_entregues / total_pedidos) * 100

print("\nAnálise de entregas:")
print(f"Total de pedidos: {total_pedidos}")
print(f"Pedidos entregues: {pedidos_entregues}")
print(f"Porcentagem de pedidos entregues: {porcentagem_entregues:.2f}%")


# Converter a coluna de compra para o formato de data
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"],
    errors="coerce"
)

print("\nTipo de dado da data da compra:")
print(df["order_purchase_timestamp"].dtype)

print("\nData da primeira compra:")
print(df["order_purchase_timestamp"].min())

print("\nData da última compra:")
print(df["order_purchase_timestamp"].max())


# Criar uma coluna com o mês da compra
df["mes_compra"] = df["order_purchase_timestamp"].dt.to_period("M")

# Contar a quantidade de pedidos por mês
pedidos_por_mes = df.groupby("mes_compra")["order_id"].count()

print("\nQuantidade de pedidos por mês:")
print(pedidos_por_mes)


print("\nQuantidade de pedidos nos últimos meses:")

print(
    df.groupby(df["order_purchase_timestamp"].dt.strftime("%Y-%m"))[
        "order_id"
    ].count().tail(8)
)

print("\nQuantidade de datas ausentes:")
print(df["order_purchase_timestamp"].isnull().sum())


# Criar uma coluna com o ano da compra
df["ano_compra"] = df["order_purchase_timestamp"].dt.year

# Contar os pedidos por ano
pedidos_por_ano = df.groupby("ano_compra")["order_id"].count()

print("\nQuantidade de pedidos por ano:")
print(pedidos_por_ano)

# Investigar os pedidos de setembro e outubro de 2018

print("\nPedidos de setembro de 2018:")

print(
    df[
        (df["order_purchase_timestamp"] >= "2018-09-01")
        & (df["order_purchase_timestamp"] < "2018-10-01")
    ][
        ["order_id", "order_status", "order_purchase_timestamp"]
    ].to_string(index=False)
)

print("\nPedidos de outubro de 2018:")

print(
    df[
        (df["order_purchase_timestamp"] >= "2018-10-01")
        & (df["order_purchase_timestamp"] < "2018-11-01")
    ][
        ["order_id", "order_status", "order_purchase_timestamp"]
    ].to_string(index=False)
)

# Analisar os status dos pedidos por mês

print("\nStatus dos pedidos por mês:")

status_por_mes = pd.crosstab(
    df["order_purchase_timestamp"].dt.to_period("M"),
    df["order_status"]
)

print(status_por_mes.tail(12))

# Calcular o tempo de entrega dos pedidos

df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"],
    errors="coerce"
)

df["tempo_entrega_dias"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Considerar apenas pedidos entregues com datas válidas
pedidos_com_entrega = df[
    (df["order_status"] == "delivered")
    & (df["tempo_entrega_dias"].notna())
]

print("\nAnálise do tempo de entrega:")

print(
    pedidos_com_entrega["tempo_entrega_dias"].describe().round(2)
)

# Converter a data estimada de entrega

df["order_estimated_delivery_date"] = pd.to_datetime(
    df["order_estimated_delivery_date"],
    errors="coerce"
)

# Selecionar pedidos entregues com as duas datas disponíveis

pedidos_entregues = df[
    (df["order_status"] == "delivered")
    & (df["order_delivered_customer_date"].notna())
    & (df["order_estimated_delivery_date"].notna())
].copy()

# Calcular a diferença entre a entrega real e a estimada

pedidos_entregues["dias_em_relacao_ao_prazo"] = (
    pedidos_entregues["order_delivered_customer_date"]
    - pedidos_entregues["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# Classificar as entregas

entregas_no_prazo = (
    pedidos_entregues["dias_em_relacao_ao_prazo"] <= 0
).sum()

entregas_atrasadas = (
    pedidos_entregues["dias_em_relacao_ao_prazo"] > 0
).sum()

total_entregas_analisadas = len(pedidos_entregues)

print("\nAnálise de entregas no prazo:")

print(f"Total de entregas analisadas: {total_entregas_analisadas}")
print(f"Entregas no prazo ou antecipadas: {entregas_no_prazo}")
print(f"Entregas atrasadas: {entregas_atrasadas}")

if total_entregas_analisadas > 0:
    print(
        f"Percentual no prazo: "
        f"{entregas_no_prazo / total_entregas_analisadas * 100:.2f}%"
    )

    print(
        f"Percentual atrasado: "
        f"{entregas_atrasadas / total_entregas_analisadas * 100:.2f}%"
    )
else:
    print("Não há entregas suficientes para calcular os percentuais.")

# Calcular a quantidade de pedidos por mês

pedidos_por_mes_grafico = df.groupby(
df["order_purchase_timestamp"].dt.to_period("M")
)["order_id"].count()

print("\n--- VERIFICAÇÃO DOS ÚLTIMOS MESES ---")
print(df["order_purchase_timestamp"].max())
print(df["order_purchase_timestamp"].dt.year.value_counts().sort_index())
print(df["order_purchase_timestamp"].dt.to_period("M").value_counts().sort_index().tail(6))

# Converter os meses para texto

pedidos_por_mes_grafico.index = (
pedidos_por_mes_grafico.index.astype(str)
)

# Identificar o mês com mais pedidos

indice_pico = pedidos_por_mes_grafico.values.argmax()
mes_maior_quantidade = pedidos_por_mes_grafico.index[indice_pico]
maior_quantidade = pedidos_por_mes_grafico.iloc[indice_pico]

# Criar o gráfico

plt.figure(figsize=(14, 7))

plt.plot(
range(len(pedidos_por_mes_grafico)),
pedidos_por_mes_grafico.values,
marker="o",
markersize=5,
linewidth=2,
label="Pedidos por mês"
)

# Exibir os meses no eixo horizontal

plt.xticks(
range(len(pedidos_por_mes_grafico)),
pedidos_por_mes_grafico.index,
rotation=45,
ha="right"
)

# Destacar o mês com mais pedidos

plt.annotate(
f"Pico: {maior_quantidade} pedidos",
xy=(indice_pico, maior_quantidade),
xytext=(0, 25),
textcoords="offset points",
ha="center",
fontsize=10,
arrowprops={"arrowstyle": "->"}
)

# Configurar o título e os nomes dos eixos

plt.title(
"Evolução mensal da quantidade de pedidos",
fontsize=16,
pad=25
)

plt.xlabel(
"Mês",
fontsize=12,
labelpad=12
)

plt.ylabel(
"Quantidade de pedidos",
fontsize=12,
labelpad=12
)

# Melhorar a organização visual

plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# Ajustar os espaçamentos

plt.tight_layout(pad=2.0)

# Exibir o gráfico

plt.show()


# Carregar os dados dos itens dos pedidos
itens = pd.read_csv("dados/olist_order_items_dataset.csv")
produtos = pd.read_csv("dados/olist_products_dataset.csv")


# Exibir as primeiras linhas
print("\n--- PRIMEIROS ITENS DOS PEDIDOS ---")
print(itens.head())

# Exibir os nomes das colunas
print("\n--- COLUNAS DOS ITENS ---")
print(itens.columns.tolist())

# Exibir informações gerais
print("\n--- INFORMAÇÕES DOS ITENS ---")
print(itens.info())

# Investigar os pedidos dos últimos meses

print("\n--- STATUS DOS PEDIDOS DE SETEMBRO E OUTUBRO DE 2018 ---")

ultimos_meses = df[
    df["order_purchase_timestamp"].dt.strftime("%Y-%m").isin(
        ["2018-09", "2018-10"]
    )
]

print(
    ultimos_meses.groupby(
        ultimos_meses["order_purchase_timestamp"].dt.strftime("%Y-%m")
    )["order_status"].value_counts()
)

print("\nTotal de pedidos encontrados nesses meses:")
print(len(ultimos_meses))

print("\nPedidos duplicados:")
print(df["order_id"].duplicated().sum())




print(
    ultimos_meses.groupby(
        ultimos_meses["order_purchase_timestamp"].dt.to_period("M")
    )["order_status"].value_counts()
)

print("\nTotal de pedidos encontrados nesses meses:")
print(len(ultimos_meses))

print("\nPedidos duplicados:")
print(df["order_id"].duplicated().sum())


print("\n--- ANÁLISE DOS ITENS DOS PEDIDOS ---")

print("\nQuantidade total de itens:")
print(len(itens))

print("\nValor total dos itens:")
print(f"R$ {itens['price'].sum():,.2f}")

print("\nValor total do frete:")
print(f"R$ {itens['freight_value'].sum():,.2f}")

print("\nPreço médio dos itens:")
print(f"R$ {itens['price'].mean():,.2f}")

print("\nCinco itens mais caros:")
print(
    itens.nlargest(5, "price")[
        ["order_id", "product_id", "price", "freight_value"]
    ]
)


print("\n--- PRODUTOS COM MAIS ITENS VENDIDOS ---")

quantidade_por_produto = itens["product_id"].value_counts()

print("\nOs 10 produtos mais frequentes:")
print(quantidade_por_produto.head(10))


print("\n--- PRODUTOS COM MAIOR VALOR TOTAL ---")

valor_por_produto = (
    itens.groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\nOs 10 produtos com maior valor acumulado:")
print(valor_por_produto.head(10))

print("\n--- TABELA DE PRODUTOS ---")

print(produtos.head())

print("\nColunas disponíveis:")
print(produtos.columns.tolist())

print("\nQuantidade de produtos cadastrados:")
print(len(produtos))


print("\n--- ANÁLISE POR CATEGORIA DE PRODUTO ---")

# Relacionar os itens dos pedidos com os produtos
itens_com_produtos = itens.merge(
    produtos[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Contar os itens por categoria
quantidade_por_categoria = (
    itens_com_produtos["product_category_name"]
    .fillna("Sem categoria")
    .value_counts()
)

print("\n10 categorias com mais itens:")
print(quantidade_por_categoria.head(10))


# Somar os preços dos itens por categoria
valor_por_categoria = (
    itens_com_produtos
    .groupby("product_category_name", dropna=False)["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\n10 categorias com maior valor acumulado:")
print(valor_por_categoria.head(10))

# Selecionar as 10 categorias com maior valor acumulado
top_10_categorias = (
    valor_por_categoria.dropna()
    .head(10)
    .sort_values()
)

# Criar o gráfico
plt.figure(figsize=(12, 7))

# Traduzir e melhorar a apresentação dos nomes das categorias
nomes_categorias = {
    "beleza_saude": "Beleza e Saúde",
    "relogios_presentes": "Relógios e Presentes",
    "cama_mesa_banho": "Cama, Mesa e Banho",
    "esporte_lazer": "Esporte e Lazer",
    "informatica_acessorios": "Informática e Acessórios",
    "moveis_decoracao": "Móveis e Decoração",
    "cool_stuff": "Produtos Diferenciados",
    "utilidades_domesticas": "Utilidades Domésticas",
    "automotivo": "Automotivo",
    "ferramentas_jardim": "Ferramentas e Jardim"
}

# Substituir os nomes somente na visualização do gráfico
top_10_categorias.index = top_10_categorias.index.map(
    lambda categoria: nomes_categorias.get(categoria, categoria)
)

ax = top_10_categorias.plot(kind="barh")

# Adicionar os valores no final de cada barra
for barra in ax.patches:
    valor = barra.get_width()

    ax.annotate(
       
        f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),

        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

# Configurar o gráfico
plt.title("Top 10 categorias por valor acumulado")
plt.xlabel("Valor acumulado (R$)")
plt.ylabel("Categoria")

# Reservar espaço para os valores das barras
plt.xlim(right=top_10_categorias.max() * 1.18)

plt.tight_layout()
print("NOVO GRÁFICO COM VALORES EM REAIS")
plt.show()

# Gráfico das 10 categorias com mais itens vendidos

itens_por_categoria = (
    itens_com_produtos["product_category_name"]
    .fillna("Sem categoria")
    .value_counts()
)

top_10_itens = itens_por_categoria.head(10).sort_values()

top_10_itens.index = top_10_itens.index.map(
    lambda categoria: nomes_categorias.get(
        categoria,
        categoria.replace("_", " ").title()
    )
)

plt.figure(figsize=(12, 7))

ax = top_10_itens.plot(kind="barh")

for barra in ax.patches:
    quantidade = int(barra.get_width())

    ax.annotate(
        f"{quantidade:,}".replace(",", "."),
        (quantidade, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 categorias por quantidade de itens")
plt.xlabel("Quantidade de itens")
plt.ylabel("Categoria")
plt.xlim(right=top_10_itens.max() * 1.15)
plt.tight_layout()
plt.show()

print("\n--- DADOS DOS CLIENTES ---")
print(clientes.head())

print("\nColunas disponíveis:")
print(clientes.columns.tolist())

# --- ANÁLISE DE CLIENTES POR ESTADO ---

print("\n--- QUANTIDADE DE CLIENTES POR ESTADO ---")

clientes_por_estado = clientes["customer_state"].value_counts()

print(clientes_por_estado)

# Gráfico dos 10 estados com mais clientes
top_10_estados = clientes_por_estado.head(10).sort_values()

plt.figure(figsize=(12, 7))

ax = top_10_estados.plot(kind="barh")

for barra in ax.patches:
    quantidade = int(barra.get_width())

    ax.annotate(
        f"{quantidade:,}".replace(",", "."),
        (quantidade, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 estados com mais clientes")
plt.xlabel("Quantidade de clientes")
plt.ylabel("Estado")
plt.xlim(right=top_10_estados.max() * 1.15)
plt.tight_layout()
plt.show()

# --- VALOR DOS PRODUTOS POR ESTADO ---

print("\n--- VALOR ACUMULADO DOS PRODUTOS POR ESTADO ---")

# Relacionar pedidos aos clientes
pedidos_clientes = df.merge(
    clientes[["customer_id", "customer_state"]],
    on="customer_id",
    how="left"
)

# Relacionar os pedidos aos itens e seus preços
pedidos_com_itens = pedidos_clientes.merge(
    itens[["order_id", "price"]],
    on="order_id",
    how="inner"
)

# Somar os preços dos itens por estado
valor_por_estado = (
    pedidos_com_itens
    .groupby("customer_state")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(valor_por_estado.head(10))

# Criar gráfico dos 10 estados com maior valor acumulado
top_10_valor_estados = valor_por_estado.head(10).sort_values()

plt.figure(figsize=(12, 7))

ax = top_10_valor_estados.plot(kind="barh")

for barra in ax.patches:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 estados por valor acumulado dos produtos")
plt.xlabel("Valor acumulado (R$)")
plt.ylabel("Estado")
plt.xlim(right=top_10_valor_estados.max() * 1.20)
plt.tight_layout()
plt.show()

# --- VALOR MÉDIO DOS ITENS POR PEDIDO EM CADA ESTADO ---

print("\n--- VALOR MÉDIO DOS ITENS POR PEDIDO POR ESTADO ---")

# Calcular o valor total dos itens de cada pedido
valor_por_pedido = (
    pedidos_com_itens
    .groupby(["customer_state", "order_id"])["price"]
    .sum()
    .reset_index(name="valor_pedido")
)

# Calcular a média dos pedidos de cada estado
media_por_estado = (
    valor_por_pedido
    .groupby("customer_state")["valor_pedido"]
    .mean()
    .sort_values(ascending=False)
)

print("\n10 estados com maior valor médio por pedido:")
print(media_por_estado.head(10).round(2))

# Selecionar os 10 primeiros e ordenar para o gráfico
top_10_media = media_por_estado.head(10).sort_values()

plt.figure(figsize=(12, 7))

ax = top_10_media.plot(kind="barh")

for barra in ax.patches:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 estados por valor médio dos itens por pedido")
plt.xlabel("Valor médio por pedido (R$)")
plt.ylabel("Estado")
plt.xlim(right=top_10_media.max() * 1.20)
plt.tight_layout()
plt.show()

# --- ANÁLISE SOMENTE DOS PEDIDOS ENTREGUES ---

print("\n--- ANÁLISE DOS PEDIDOS ENTREGUES ---")

# Selecionar somente pedidos entregues
pedidos_entregues = df[df["order_status"] == "delivered"].copy()

print("Quantidade de pedidos entregues:")
print(pedidos_entregues["order_id"].nunique())

# Relacionar os pedidos entregues aos clientes
entregues_com_clientes = pedidos_entregues.merge(
    clientes[["customer_id", "customer_state"]],
    on="customer_id",
    how="left"
)

# Relacionar os pedidos entregues aos itens
itens_entregues = entregues_com_clientes.merge(
    itens[["order_id", "price"]],
    on="order_id",
    how="inner"
)

# Calcular o valor dos itens de cada pedido
valor_pedido_entregue = (
    itens_entregues
    .groupby(["customer_state", "order_id"])["price"]
    .sum()
    .reset_index(name="valor_pedido")
)

# Calcular a média por estado
media_entregues_por_estado = (
    valor_pedido_entregue
    .groupby("customer_state")["valor_pedido"]
    .mean()
    .sort_values(ascending=False)
)

print("\n10 estados com maior valor médio por pedido entregue:")
print(media_entregues_por_estado.head(10).round(2))

# Preparar os dados do gráfico
top_10_media_entregues = (
    media_entregues_por_estado.head(10)
    .sort_values()
)

plt.figure(figsize=(12, 7))

ax = top_10_media_entregues.plot(kind="barh")

for barra in ax.patches:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 estados por valor médio dos itens por pedido entregue")
plt.xlabel("Valor médio dos itens (R$)")
plt.ylabel("Estado")
plt.xlim(right=top_10_media_entregues.max() * 1.20)
plt.tight_layout()
plt.show()


# --- FATURAMENTO POR ESTADO: SOMENTE PEDIDOS ENTREGUES ---

print("\n--- FATURAMENTO POR ESTADO ---")

# Somar o valor dos itens entregues por estado
faturamento_por_estado = (
    itens_entregues
    .groupby("customer_state")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 estados com maior faturamento:")
print(faturamento_por_estado.head(10).round(2))

# Selecionar os 10 estados com maior faturamento
top_10_faturamento = (
    faturamento_por_estado.head(10)
    .sort_values()
)

# Criar o gráfico
plt.figure(figsize=(12, 7))

ax = top_10_faturamento.plot(kind="barh")

# Adicionar os valores nas barras
for barra in ax.patches:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 estados por faturamento de pedidos entregues")
plt.xlabel("Faturamento dos itens (R$)")
plt.ylabel("Estado")
plt.xlim(right=top_10_faturamento.max() * 1.20)
plt.tight_layout()
plt.show()


# --- EVOLUÇÃO MENSAL DO FATURAMENTO ---

print("\n--- EVOLUÇÃO MENSAL DO FATURAMENTO ---")

# Selecionar somente pedidos entregues
entregues = df[df["order_status"] == "delivered"].copy()

# Converter a data de compra para o formato de data
entregues["order_purchase_timestamp"] = pd.to_datetime(
    entregues["order_purchase_timestamp"]
)

# Relacionar os pedidos entregues aos itens
itens_entregues_mensal = entregues[["order_id", "order_purchase_timestamp"]].merge(
    itens[["order_id", "price"]],
    on="order_id",
    how="inner"
)

# Criar uma coluna com o mês da compra
itens_entregues_mensal["mes"] = (
    itens_entregues_mensal["order_purchase_timestamp"]
    .dt.to_period("M")
)

# Somar os preços dos itens por mês
faturamento_mensal = (
    itens_entregues_mensal
    .groupby("mes")["price"]
    .sum()
)

print("\nFaturamento por mês:")
print(faturamento_mensal.round(2))

# Criar o gráfico
plt.figure(figsize=(14, 7))

ax = faturamento_mensal.plot(kind="line", marker="o")

plt.title("Evolução mensal do faturamento dos pedidos entregues")
plt.xlabel("Mês da compra")
plt.ylabel("Faturamento dos itens (R$)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- FATURAMENTO POR CATEGORIA: PEDIDOS ENTREGUES ---

print("\n--- FATURAMENTO POR CATEGORIA ---")

# Selecionar somente pedidos entregues
pedidos_entregues_categoria = df[
    df["order_status"] == "delivered"
][["order_id"]].copy()

# Relacionar os pedidos entregues aos itens
itens_entregues_categoria = pedidos_entregues_categoria.merge(
    itens[["order_id", "product_id", "price"]],
    on="order_id",
    how="inner"
)

# Relacionar os itens às categorias dos produtos
itens_entregues_categoria = itens_entregues_categoria.merge(
    produtos[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Somar o faturamento por categoria
faturamento_categoria_entregue = (
    itens_entregues_categoria
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\n10 categorias com maior faturamento:")
print(faturamento_categoria_entregue.head(10).round(2))

# Selecionar as 10 categorias com maior faturamento
top_10_categorias_entregues = (
    faturamento_categoria_entregue.head(10)
    .sort_values()
)

# Traduzir os nomes das categorias, se houver um dicionário disponível
nomes_grafico = top_10_categorias_entregues.copy()

if "nomes_categorias" in globals():
    nomes_grafico.index = [
        nomes_categorias.get(categoria, categoria)
        for categoria in nomes_grafico.index
    ]

# Criar o gráfico
plt.figure(figsize=(12, 7))

ax = nomes_grafico.plot(kind="barh")

for barra in ax.patches:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 categorias por faturamento de pedidos entregues")
plt.xlabel("Faturamento dos itens (R$)")
plt.ylabel("Categoria")
plt.xlim(right=nomes_grafico.max() * 1.20)
plt.tight_layout()
plt.show()


# --- PREÇO MÉDIO POR CATEGORIA: PEDIDOS ENTREGUES ---

print("\n--- PREÇO MÉDIO POR CATEGORIA ---")

# Calcular o preço médio dos itens por categoria
preco_medio_categoria = (
    itens_entregues_categoria
    .groupby("product_category_name")["price"]
    .mean()
    .sort_values(ascending=False)
)

print("\n10 categorias com maior preço médio:")
print(preco_medio_categoria.head(10).round(2))

# Selecionar as 10 categorias com maior preço médio
top_10_preco_medio = (
    preco_medio_categoria.head(10)
    .sort_values()
)

# Preparar os nomes das categorias para o gráfico
nomes_grafico = top_10_preco_medio.copy()

if "nomes_categorias" in globals():
    nomes_grafico.index = [
        nomes_categorias.get(categoria, categoria)
        for categoria in nomes_grafico.index
    ]

# Criar o gráfico
plt.figure(figsize=(12, 7))

ax = nomes_grafico.plot(kind="barh")

# Adicionar os valores nas barras
for barra in ax.patches:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Top 10 categorias por preço médio dos itens entregues")
plt.xlabel("Preço médio (R$)")
plt.ylabel("Categoria")
plt.xlim(right=nomes_grafico.max() * 1.20)
plt.tight_layout()
plt.show()

# --- QUANTIDADE MENSAL DE PEDIDOS ENTREGUES ---

print("\n--- QUANTIDADE MENSAL DE PEDIDOS ENTREGUES ---")

# Selecionar somente pedidos entregues
pedidos_entregues_mes = df[
    df["order_status"] == "delivered"
].copy()

# Converter a data da compra para o formato de data
pedidos_entregues_mes["order_purchase_timestamp"] = pd.to_datetime(
    pedidos_entregues_mes["order_purchase_timestamp"]
)

# Agrupar os pedidos pelo mês da compra
quantidade_pedidos_mensal = (
    pedidos_entregues_mes
    .groupby(
        pedidos_entregues_mes["order_purchase_timestamp"].dt.to_period("M")
    )["order_id"]
    .nunique()
)

print("\nQuantidade de pedidos entregues por mês:")
print(quantidade_pedidos_mensal)

# Criar o gráfico
plt.figure(figsize=(14, 7))

ax = quantidade_pedidos_mensal.plot(
    kind="line",
    marker="o"
)

plt.title("Quantidade mensal de pedidos entregues")
plt.xlabel("Mês da compra")
plt.ylabel("Quantidade de pedidos")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# --- VALOR MÉDIO MENSAL POR PEDIDO ENTREGUE ---

print("\n--- VALOR MÉDIO MENSAL POR PEDIDO ENTREGUE ---")

# Dividir o faturamento mensal pela quantidade de pedidos
valor_medio_mensal = (
    faturamento_mensal / quantidade_pedidos_mensal
).dropna()

print("\nValor médio dos itens por pedido em cada mês:")
print(valor_medio_mensal.round(2))

# Criar o gráfico
plt.figure(figsize=(14, 7))

ax = valor_medio_mensal.plot(
    kind="line",
    marker="o"
)

plt.title("Valor médio dos itens por pedido entregue em cada mês")
plt.xlabel("Mês da compra")
plt.ylabel("Valor médio por pedido (R$)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# --- PRODUTOS MAIS VENDIDOS: PEDIDOS ENTREGUES ---

print("\n--- PRODUTOS MAIS VENDIDOS ---")

# Selecionar somente pedidos entregues
pedidos_entregues_produtos = df[
    df["order_status"] == "delivered"
][["order_id"]].copy()

# Relacionar os pedidos aos itens vendidos
itens_entregues_produtos = pedidos_entregues_produtos.merge(
    itens[["order_id", "product_id"]],
    on="order_id",
    how="inner"
)

# Contar quantas vezes cada produto aparece nos itens entregues
quantidade_por_produto = (
    itens_entregues_produtos
    .groupby("product_id")
    .size()
    .sort_values(ascending=False)
)

# Relacionar os produtos aos seus nomes e categorias
ranking_produtos = quantidade_por_produto.rename(
    "quantidade_vendida"
).reset_index()

ranking_produtos = ranking_produtos.merge(
    produtos[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Mostrar os 10 produtos mais vendidos
top_10_produtos = ranking_produtos.head(10)

print("\n10 produtos com maior quantidade de itens vendidos:")
print(top_10_produtos.to_string(index=False))

# Preparar os dados para o gráfico
grafico_produtos = (
    top_10_produtos
    .sort_values("quantidade_vendida")
    .copy()
)

grafico_produtos["rotulo"] = (
    grafico_produtos["product_id"].str[:8]
    + " - "
    + grafico_produtos["product_category_name"].fillna("Sem categoria")
)

# Criar o gráfico
plt.figure(figsize=(12, 7))

ax = plt.barh(
    grafico_produtos["rotulo"],
    grafico_produtos["quantidade_vendida"]
)

for barra in ax:
    valor = barra.get_width()

    plt.annotate(
        str(int(valor)),
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center"
    )

plt.title("Top 10 produtos por quantidade de itens em pedidos entregues")
plt.xlabel("Quantidade de itens vendidos")
plt.ylabel("Produto (ID abreviado e categoria)")
plt.tight_layout()
plt.show()

# --- FATURAMENTO DOS PRODUTOS MAIS VENDIDOS ---

print("\n--- FATURAMENTO DOS PRODUTOS MAIS VENDIDOS ---")

# Somar o faturamento de cada produto
faturamento_por_produto = (
    itens_entregues_produtos
    .merge(
        itens[["order_id", "product_id", "price"]],
        on=["order_id", "product_id"],
        how="left"
    )
    .groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

# Selecionar os 10 produtos com maior quantidade vendida
ids_top_vendidos = top_10_produtos["product_id"]

# Obter o faturamento desses produtos
faturamento_top_vendidos = (
    faturamento_por_produto
    .reindex(ids_top_vendidos)
    .rename("faturamento")
    .reset_index()
)

# Adicionar a quantidade vendida
faturamento_top_vendidos = faturamento_top_vendidos.merge(
    top_10_produtos[["product_id", "quantidade_vendida"]],
    on="product_id",
    how="left"
)

# Ordenar pelo faturamento, do maior para o menor
faturamento_top_vendidos = faturamento_top_vendidos.sort_values(
    "faturamento",
    ascending=False
)

print("\nFaturamento dos 10 produtos mais vendidos:")
print(
    faturamento_top_vendidos.to_string(
        index=False,
        formatters={
            "faturamento": lambda valor: (
                f"R$ {valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
        }
    )
)

# Preparar os dados para o gráfico
grafico_faturamento = faturamento_top_vendidos.copy()

grafico_faturamento["rotulo"] = (
    grafico_faturamento["product_id"].str[:8]
)

grafico_faturamento = grafico_faturamento.sort_values("faturamento")

# Criar o gráfico
plt.figure(figsize=(12, 7))

ax = plt.barh(
    grafico_faturamento["rotulo"],
    grafico_faturamento["faturamento"]
)

for barra in ax:
    valor = barra.get_width()

    rotulo = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    plt.annotate(
        rotulo,
        (valor, barra.get_y() + barra.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.title("Faturamento dos 10 produtos mais vendidos")
plt.xlabel("Faturamento dos itens (R$)")
plt.ylabel("ID do produto (abreviado)")
plt.xlim(right=grafico_faturamento["faturamento"].max() * 1.25)
plt.tight_layout()
plt.show()

# 10 produtos com maior faturamento entre todos os produtos

print("\n--- 10 PRODUTOS COM MAIOR FATURAMENTO ---")

# Seleciona os 10 produtos que geraram mais faturamento
top_10_faturamento_todos = (
    faturamento_por_produto
    .sort_values(ascending=False)
    .head(10)
    .rename("faturamento")
    .reset_index()
)

# Calcula a quantidade vendida de cada produto
quantidade_todos_produtos = (
    itens_entregues_produtos
    .groupby("product_id")
    .size()
    .rename("quantidade_vendida")
    .reset_index()
)

# Adiciona a quantidade vendida à tabela dos 10 produtos
top_10_faturamento_todos = top_10_faturamento_todos.merge(
    quantidade_todos_produtos,
    on="product_id",
    how="left"
)

# Adiciona a categoria de cada produto
top_10_faturamento_todos = top_10_faturamento_todos.merge(
    produtos[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Organiza as colunas para facilitar a leitura
top_10_faturamento_todos = top_10_faturamento_todos[
    [
        "product_id",
        "product_category_name",
        "quantidade_vendida",
        "faturamento"
    ]
]

# Exibe os resultados
print(top_10_faturamento_todos.to_string(index=False))

# Investigar o produto com maior faturamento

print("\n--- INVESTIGAÇÃO DO PRODUTO COM MAIOR FATURAMENTO ---")

produto_investigado = "5769ef0a239114ac3a854af00df129e4"

# Buscar as informações do produto
dados_produto = produtos[
    produtos["product_id"] == produto_investigado
]

print("\nInformações do produto:")
print(dados_produto.to_string(index=False))

# Buscar os itens vendidos desse produto
itens_investigados = itens_entregues_produtos[
    itens_entregues_produtos["product_id"] == produto_investigado
].merge(
    itens[["order_id", "product_id", "price", "freight_value"]],
    on=["order_id", "product_id"],
    how="left"
)

print("\nItens vendidos:")
print(
    itens_investigados[
        ["order_id", "product_id", "price", "freight_value"]
    ].to_string(index=False)
)

print("\nQuantidade de itens encontrados:", len(itens_investigados))

print(
    "Soma dos preços: R$",
    round(itens_investigados["price"].sum(), 2)
)

print(
    "Soma dos fretes: R$",
    round(itens_investigados["freight_value"].sum(), 2)
)

print(
    "Preço médio por unidade: R$",
    round(itens_investigados["price"].mean(), 2)
)

# Corrigir o cálculo do faturamento por produto

print("\n--- FATURAMENTO CORRIGIDO POR PRODUTO ---")

# Junta os pedidos entregues diretamente com os itens
itens_entregues_corretos = pedidos_entregues[["order_id"]].merge(
    itens,
    on="order_id",
    how="inner"
)

# Calcula o faturamento de cada produto sem duplicar as junções
faturamento_por_produto_corrigido = (
    itens_entregues_corretos
    .groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

# Seleciona os 10 produtos com maior faturamento
top_10_faturamento_corrigido = (
    faturamento_por_produto_corrigido
    .head(10)
    .rename("faturamento")
    .reset_index()
)

# Conta a quantidade de unidades vendidas por produto
quantidade_produtos_corrigida = (
    itens_entregues_corretos
    .groupby("product_id")
    .size()
    .rename("quantidade_vendida")
    .reset_index()
)

# Adiciona a quantidade e a categoria
top_10_faturamento_corrigido = (
    top_10_faturamento_corrigido
    .merge(
        quantidade_produtos_corrigida,
        on="product_id",
        how="left"
    )
    .merge(
        produtos[["product_id", "product_category_name"]],
        on="product_id",
        how="left"
    )
)

print(top_10_faturamento_corrigido.to_string(index=False))

# Confere o produto que investigamos
produto_investigado = "5769ef0a239114ac3a854af00df129e4"

print("\n--- CONFERÊNCIA DO PRODUTO INVESTIGADO ---")

print(
    "Quantidade vendida:",
    len(
        itens_entregues_corretos[
            itens_entregues_corretos["product_id"] == produto_investigado
        ]
    )
)

print(
    "Faturamento correto: R$",
    round(
        faturamento_por_produto_corrigido.get(produto_investigado, 0),
        2
    )
)

# Análise de faturamento por categoria de produto

print("\n--- FATURAMENTO POR CATEGORIA ---")

# Adiciona a categoria de cada produto aos itens vendidos
itens_com_categorias_corrigidos = itens_entregues_corretos.merge(
    produtos[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Calcula o faturamento total de cada categoria
faturamento_por_categoria_corrigido = (
    itens_com_categorias_corrigidos
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

# Seleciona as 10 categorias com maior faturamento
top_10_categorias_faturamento = (
    faturamento_por_categoria_corrigido
    .head(10)
)

# Exibe o resultado no terminal
print("\n10 categorias com maior faturamento:")

for categoria, faturamento in top_10_categorias_faturamento.items():
    print(f"{categoria}: R$ {faturamento:,.2f}")

# Cria um gráfico de barras
plt.figure(figsize=(12, 7))

top_10_categorias_faturamento.sort_values().plot(
    kind="barh"
)

plt.title("10 categorias com maior faturamento")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Categoria")
plt.tight_layout()

plt.show()


# Análise de quantidade vendida por categoria

print("\n--- QUANTIDADE VENDIDA POR CATEGORIA ---")

# Conta quantos itens foram vendidos em cada categoria
quantidade_por_categoria = (
    itens_com_categorias_corrigidos
    .groupby("product_category_name")
    .size()
    .sort_values(ascending=False)
)

# Seleciona as 10 categorias com mais itens vendidos
top_10_quantidade_categorias = quantidade_por_categoria.head(10)

# Exibe o ranking no terminal
for categoria, quantidade in top_10_quantidade_categorias.items():
    print(f"{categoria}: {quantidade:,} itens")

# Cria um gráfico de barras horizontais
plt.figure(figsize=(12, 7))

top_10_quantidade_categorias.sort_values().plot(kind="barh")

plt.title("10 categorias com maior quantidade de itens vendidos")
plt.xlabel("Quantidade de itens vendidos")
plt.ylabel("Categoria")
plt.tight_layout()

plt.show()

# Análise do faturamento médio por item em cada categoria

print("\n--- FATURAMENTO MÉDIO POR ITEM E CATEGORIA ---")

# Calcula o faturamento total de cada categoria
faturamento_categoria = (
    itens_com_categorias_corrigidos
    .groupby("product_category_name")["price"]
    .sum()
)

# Calcula a quantidade de itens vendidos por categoria
quantidade_categoria = (
    itens_com_categorias_corrigidos
    .groupby("product_category_name")
    .size()
)

# Calcula o faturamento médio por item
media_por_categoria = (
    faturamento_categoria / quantidade_categoria
).sort_values(ascending=False)

# Seleciona as 10 categorias com maior média
top_10_media_categoria = media_por_categoria.head(10)

# Exibe os resultados
for categoria, media in top_10_media_categoria.items():
    print(f"{categoria}: R$ {media:,.2f} por item")

# Cria um gráfico de barras horizontais
plt.figure(figsize=(12, 7))

top_10_media_categoria.sort_values().plot(kind="barh")

plt.title("10 categorias com maior faturamento médio por item")
plt.xlabel("Faturamento médio por item (R$)")
plt.ylabel("Categoria")
plt.tight_layout()

plt.show()

# Análise da evolução mensal do faturamento

print("\n--- EVOLUÇÃO MENSAL DO FATURAMENTO ---")

# Organiza os dados em ordem cronológica
faturamento_mensal_ordenado = faturamento_mensal.sort_index()

# Exibe o faturamento de cada mês
for mes, faturamento in faturamento_mensal_ordenado.items():
    print(f"{mes}: R$ {faturamento:,.2f}")

# Identifica o mês de maior faturamento
mes_maior_faturamento = faturamento_mensal_ordenado.idxmax()
maior_faturamento = faturamento_mensal_ordenado.max()

print("\nMês com maior faturamento registrado:")
print(f"{mes_maior_faturamento}: R$ {maior_faturamento:,.2f}")

# Identifica o mês de menor faturamento registrado
mes_menor_faturamento = faturamento_mensal_ordenado.idxmin()
menor_faturamento = faturamento_mensal_ordenado.min()

print("\nMês com menor faturamento registrado:")
print(f"{mes_menor_faturamento}: R$ {menor_faturamento:,.2f}")

# Cria o gráfico de evolução mensal
plt.figure(figsize=(14, 7))

faturamento_mensal_ordenado.plot(
    kind="line",
    marker="o"
)

plt.title("Evolução mensal do faturamento da Olist")
plt.xlabel("Mês da compra")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()

# Comparação entre faturamento e quantidade de pedidos por mês

print("\n--- FATURAMENTO E QUANTIDADE DE PEDIDOS POR MÊS ---")

# Junta o faturamento mensal com a quantidade de pedidos
comparacao_mensal = pd.concat(
    [
        faturamento_mensal,
        quantidade_pedidos_mensal
    ],
    axis=1
)

# Define nomes para as colunas
comparacao_mensal.columns = [
    "faturamento",
    "quantidade_pedidos"
]

# Organiza os meses em ordem cronológica
comparacao_mensal = comparacao_mensal.sort_index()

# Exibe os resultados
print(comparacao_mensal.to_string())

# Identifica o mês com mais pedidos
mes_mais_pedidos = comparacao_mensal["quantidade_pedidos"].idxmax()

maior_quantidade_pedidos = comparacao_mensal[
    "quantidade_pedidos"
].max()

print("\nMês com maior quantidade de pedidos:")
print(f"{mes_mais_pedidos}: {maior_quantidade_pedidos} pedidos")

# Gráfico comparativo de faturamento e quantidade de pedidos

print("\n--- GRÁFICO COMPARATIVO MENSAL ---")

fig, ax1 = plt.subplots(figsize=(14, 7))

# Primeiro eixo: faturamento
ax1.plot(
    comparacao_mensal.index.astype(str),
    comparacao_mensal["faturamento"],
    marker="o",
    label="Faturamento"
)

ax1.set_xlabel("Mês da compra")
ax1.set_ylabel("Faturamento (R$)")
ax1.tick_params(axis="x", rotation=45)
ax1.grid(True)

# Segundo eixo: quantidade de pedidos
ax2 = ax1.twinx()

ax2.plot(
    comparacao_mensal.index.astype(str),
    comparacao_mensal["quantidade_pedidos"],
    marker="s",
    label="Quantidade de pedidos"
)

ax2.set_ylabel("Quantidade de pedidos")

# Combina as legendas dos dois eixos
linha1, legenda1 = ax1.get_legend_handles_labels()
linha2, legenda2 = ax2.get_legend_handles_labels()

ax1.legend(
    linha1 + linha2,
    legenda1 + legenda2,
    loc="upper left"
)

plt.title("Evolução mensal do faturamento e dos pedidos")
plt.tight_layout()
plt.show()

# Gráfico 1: evolução mensal do faturamento

plt.figure(figsize=(14, 6))

comparacao_mensal["faturamento"].plot(
    kind="line",
    marker="o"
)

plt.title("Evolução mensal do faturamento da Olist")
plt.xlabel("Mês da compra")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# Gráfico 2: evolução mensal da quantidade de pedidos

plt.figure(figsize=(14, 6))

comparacao_mensal["quantidade_pedidos"].plot(
    kind="line",
    marker="o"
)

plt.title("Evolução mensal da quantidade de pedidos da Olist")
plt.xlabel("Mês da compra")
plt.ylabel("Quantidade de pedidos")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Análise do faturamento por categoria de produto

print("\n--- FATURAMENTO POR CATEGORIA ---")

# Soma o preço dos itens entregues por categoria
faturamento_por_categoria = (
    itens_com_categorias_corrigidos
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

# Seleciona as 10 categorias com maior faturamento
top_10_categorias = faturamento_por_categoria.head(10)

# Exibe os resultados
print(top_10_categorias.round(2))

# Cria o gráfico das 10 categorias com maior faturamento
plt.figure(figsize=(12, 6))

top_10_categorias.sort_values().plot(kind="barh")

plt.title("Top 10 categorias por faturamento")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Categoria de produto")
plt.tight_layout()

plt.show()
































