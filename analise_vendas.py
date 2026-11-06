"""
Análise de vendas do e-commerce Olist
=====================================

Analisa pedidos, entregas, faturamento, produtos, categorias e estados
a partir dos dados públicos da Olist (Kaggle).

Como usar:
    python analise_vendas.py            # salva os gráficos na pasta imagens/
    python analise_vendas.py --mostrar  # além de salvar, abre as janelas dos gráficos

Definições usadas em todo o projeto:
    - "Faturamento" = soma do preço dos itens (price), SEM o frete.
    - Só entram nas análises de faturamento os pedidos com status "delivered".
    - O mês considerado é o mês da COMPRA, não o da entrega.
"""

import sys
from pathlib import Path

import matplotlib
import pandas as pd

MOSTRAR_GRAFICOS = "--mostrar" in sys.argv
if not MOSTRAR_GRAFICOS:
    matplotlib.use("Agg")  # modo "sem janela": só salva as imagens

import matplotlib.pyplot as plt  # noqa: E402  (precisa vir depois do matplotlib.use)

# ==========================================
# CONFIGURAÇÕES
# ==========================================

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_IMAGENS = PASTA_PROJETO / "imagens"

COLUNAS_DATA = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

# Nomes mais bonitos para os gráficos (as demais categorias usam um nome automático)
NOMES_CATEGORIAS = {
    "beleza_saude": "Beleza e Saúde",
    "relogios_presentes": "Relógios e Presentes",
    "cama_mesa_banho": "Cama, Mesa e Banho",
    "esporte_lazer": "Esporte e Lazer",
    "informatica_acessorios": "Informática e Acessórios",
    "moveis_decoracao": "Móveis e Decoração",
    "cool_stuff": "Produtos Diferenciados",
    "utilidades_domesticas": "Utilidades Domésticas",
    "automotivo": "Automotivo",
    "ferramentas_jardim": "Ferramentas e Jardim",
    "sem_categoria": "Sem categoria",
}


# ==========================================
# FUNÇÕES AUXILIARES (formatação e gráficos)
# ==========================================

def formatar_reais(valor):
    """1234567.8 -> 'R$ 1.234.567,80'"""
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_inteiro(valor):
    """10953 -> '10.953'"""
    return f"{int(valor):,}".replace(",", ".")


def nome_bonito(categoria):
    """Converte 'cama_mesa_banho' em 'Cama, Mesa e Banho' (ou um nome automático)."""
    return NOMES_CATEGORIAS.get(categoria, str(categoria).replace("_", " ").title())


def titulo_secao(texto):
    print(f"\n{'=' * 60}\n{texto}\n{'=' * 60}")


def salvar_grafico(nome_arquivo):
    """Ajusta o layout, salva em imagens/ e (opcionalmente) mostra o gráfico."""
    plt.tight_layout()
    PASTA_IMAGENS.mkdir(exist_ok=True)
    plt.savefig(PASTA_IMAGENS / f"{nome_arquivo}.png", dpi=150)
    if MOSTRAR_GRAFICOS:
        plt.show()
    plt.close()


def grafico_barras(serie, titulo, xlabel, ylabel, arquivo, em_reais=False):
    """Barras horizontais com o valor escrito no fim de cada barra."""
    serie = serie.sort_values()
    formatar = formatar_reais if em_reais else formatar_inteiro

    _, ax = plt.subplots(figsize=(12, 7))
    barras = ax.barh(serie.index.astype(str), serie.values)

    for barra in barras:
        valor = barra.get_width()
        ax.annotate(
            formatar(valor),
            (valor, barra.get_y() + barra.get_height() / 2),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            fontsize=9,
        )

    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(right=serie.max() * 1.2)  # espaço para o texto não ser cortado
    salvar_grafico(arquivo)


def grafico_linha(serie, titulo, ylabel, arquivo, destacar_pico=True):
    """Linha ao longo dos meses, com o ponto mais alto destacado."""
    meses = serie.index.astype(str)

    _, ax = plt.subplots(figsize=(14, 7))
    ax.plot(meses, serie.values, marker="o", linewidth=2)

    if destacar_pico:
        posicao = int(serie.values.argmax())
        ax.annotate(
            f"Pico: {meses[posicao]}",
            (meses[posicao], serie.values[posicao]),
            xytext=(0, 25),
            textcoords="offset points",
            ha="center",
            arrowprops={"arrowstyle": "->"},
        )

    ax.set_title(titulo, fontsize=14)
    ax.set_xlabel("Mês da compra")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    salvar_grafico(arquivo)


def grafico_faturamento_vs_pedidos(faturamento, pedidos):
    """Dois eixos Y: faturamento (esquerda) e quantidade de pedidos (direita)."""
    meses = faturamento.index.astype(str)

    _, ax1 = plt.subplots(figsize=(14, 7))
    ax1.plot(meses, faturamento.values, marker="o", label="Faturamento")
    ax1.set_xlabel("Mês da compra")
    ax1.set_ylabel("Faturamento (R$)")
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.plot(meses, pedidos.reindex(faturamento.index).values,
             marker="s", color="tab:orange", label="Quantidade de pedidos")
    ax2.set_ylabel("Quantidade de pedidos")

    linhas1, rotulos1 = ax1.get_legend_handles_labels()
    linhas2, rotulos2 = ax2.get_legend_handles_labels()
    ax1.legend(linhas1 + linhas2, rotulos1 + rotulos2, loc="upper left")

    plt.title("Evolução mensal do faturamento e dos pedidos entregues")
    salvar_grafico("comparativo_faturamento_pedidos")


# ==========================================
# 1. CARREGAMENTO E PREPARAÇÃO
# ==========================================

def ler_csv(nome_arquivo):
    caminho = PASTA_DADOS / nome_arquivo
    if not caminho.exists():
        sys.exit(
            f"Arquivo não encontrado: {caminho}\n"
            "Baixe os dados no Kaggle (link no README) e coloque na pasta 'dados'."
        )
    return pd.read_csv(caminho)


def carregar_dados():
    pedidos = ler_csv("olist_orders_dataset.csv")
    itens = ler_csv("olist_order_items_dataset.csv")
    produtos = ler_csv("olist_products_dataset.csv")
    clientes = ler_csv("olist_customers_dataset.csv")

    for coluna in COLUNAS_DATA:
        pedidos[coluna] = pd.to_datetime(pedidos[coluna], errors="coerce")

    return pedidos, itens, produtos, clientes


def montar_itens_entregues(pedidos, itens, produtos, clientes):
    """
    Cria UMA tabela base com os itens dos pedidos entregues, já com
    estado do cliente, categoria do produto e mês da compra.

    O parâmetro validate="many_to_one" faz o pandas avisar (erro) se alguma
    junção duplicar linhas, o que mudaria os resultados sem ninguém perceber.
    """
    entregues = pedidos.loc[
        pedidos["order_status"] == "delivered",
        ["order_id", "customer_id", "order_purchase_timestamp"],
    ]

    base = (
        itens[["order_id", "product_id", "price"]]
        .merge(entregues, on="order_id", how="inner", validate="many_to_one")
        .merge(clientes[["customer_id", "customer_state"]],
               on="customer_id", how="left", validate="many_to_one")
        .merge(produtos[["product_id", "product_category_name"]],
               on="product_id", how="left", validate="many_to_one")
    )

    base["mes"] = base["order_purchase_timestamp"].dt.to_period("M")
    base["product_category_name"] = base["product_category_name"].fillna("sem_categoria")
    return base


# ==========================================
# 2. QUALIDADE DOS DADOS E PEDIDOS
# ==========================================

def verificar_qualidade(pedidos, clientes):
    titulo_secao("QUALIDADE DOS DADOS")

    print(f"Pedidos: {pedidos.shape[0]:,} linhas | Clientes: {clientes.shape[0]:,} linhas")
    print(f"Pedidos com order_id repetido: {pedidos['order_id'].duplicated().sum()}")

    print("\nValores ausentes por coluna (pedidos):")
    print(pedidos.isnull().sum())

    print("\nPedidos por status:")
    print(pedidos["order_status"].value_counts())

    percentual = (pedidos["order_status"] == "delivered").mean() * 100
    print(f"\nPedidos entregues: {percentual:.2f}% do total")


def analisar_periodo(pedidos):
    titulo_secao("PERÍODO DOS PEDIDOS")

    compras = pedidos["order_purchase_timestamp"]
    print(f"Primeira compra: {compras.min()}")
    print(f"Última compra:   {compras.max()}")

    print("\nPedidos por ano:")
    print(compras.dt.year.value_counts().sort_index())

    print("\nPedidos nos últimos 6 meses da série:")
    print(compras.dt.to_period("M").value_counts().sort_index().tail(6))
    print(
        "\nAtenção: o começo (2016) e o fim da série têm poucos pedidos. "
        "Isso pode ser limitação da base, então cuidado ao interpretar tendências."
    )

    print("\nOs 5 dias com mais pedidos:")
    print(compras.dt.date.value_counts().head(5))


# ==========================================
# 3. ENTREGAS
# ==========================================

def analisar_entregas(pedidos):
    titulo_secao("TEMPO E PRAZO DE ENTREGA")

    entregues = pedidos[
        (pedidos["order_status"] == "delivered")
        & pedidos["order_delivered_customer_date"].notna()
        & pedidos["order_estimated_delivery_date"].notna()
    ].copy()

    um_dia = pd.Timedelta(days=1)

    tempo_entrega = (
        entregues["order_delivered_customer_date"] - entregues["order_purchase_timestamp"]
    ) / um_dia
    print("Tempo de entrega (dias, da compra até o cliente receber):")
    print(tempo_entrega.describe().round(2))

    dias_vs_prazo = (
        entregues["order_delivered_customer_date"] - entregues["order_estimated_delivery_date"]
    ) / um_dia
    atrasadas = (dias_vs_prazo > 0).sum()
    total = len(entregues)

    print(f"\nEntregas analisadas: {total:,}")
    if total == 0:
        print("Não há entregas suficientes para calcular percentuais.")
        return

    print(f"No prazo ou antecipadas: {total - atrasadas:,} ({(total - atrasadas) / total:.2%})")
    print(f"Atrasadas:               {atrasadas:,} ({atrasadas / total:.2%})")


# ==========================================
# 4. FATURAMENTO MENSAL
# ==========================================

def analisar_faturamento_mensal(base, pedidos):
    titulo_secao("EVOLUÇÃO MENSAL (PEDIDOS ENTREGUES)")

    faturamento = base.groupby("mes")["price"].sum().sort_index()

    entregues = pedidos[pedidos["order_status"] == "delivered"]
    qtd_pedidos = (
        entregues.groupby(entregues["order_purchase_timestamp"].dt.to_period("M"))["order_id"]
        .nunique()
    )

    ticket_medio = (faturamento / qtd_pedidos).dropna()

    tabela = pd.DataFrame({
        "faturamento": faturamento.round(2),
        "pedidos": qtd_pedidos,
        "ticket_medio": ticket_medio.round(2),
    })
    print(tabela.to_string())

    mes_max = faturamento.idxmax()
    mes_min = faturamento.idxmin()
    print(f"\nMaior faturamento: {mes_max} -> {formatar_reais(faturamento.max())} "
          f"({qtd_pedidos.get(mes_max, 0):,} pedidos entregues)")
    print(f"Menor faturamento: {mes_min} -> {formatar_reais(faturamento.min())}")

    grafico_linha(faturamento, "Faturamento mensal dos pedidos entregues",
                  "Faturamento (R$)", "faturamento_mensal")
    grafico_linha(qtd_pedidos, "Quantidade mensal de pedidos entregues",
                  "Pedidos", "pedidos_mensais")
    grafico_linha(ticket_medio, "Valor médio dos itens por pedido entregue",
                  "Valor médio (R$)", "ticket_medio_mensal", destacar_pico=False)
    grafico_faturamento_vs_pedidos(faturamento, qtd_pedidos)


# ==========================================
# 5. PRODUTOS
# ==========================================

def analisar_produtos(base):
    titulo_secao("PRODUTOS")

    resumo = (
        base.groupby("product_id")
        .agg(
            categoria=("product_category_name", "first"),
            quantidade=("price", "size"),
            faturamento=("price", "sum"),
        )
        .reset_index()
    )
    resumo["rotulo"] = resumo["product_id"].str[:8] + " - " + resumo["categoria"].map(nome_bonito)

    mais_vendidos = resumo.nlargest(10, "quantidade")
    maior_faturamento = resumo.nlargest(10, "faturamento")

    print("10 produtos mais vendidos (quantidade):")
    print(mais_vendidos.drop(columns="rotulo").to_string(index=False))

    print("\n10 produtos com maior faturamento:")
    print(maior_faturamento.drop(columns="rotulo").to_string(index=False))

    grafico_barras(
        mais_vendidos.set_index("rotulo")["quantidade"],
        "Top 10 produtos por quantidade vendida (pedidos entregues)",
        "Quantidade de itens vendidos", "Produto (ID abreviado e categoria)",
        "top_produtos_quantidade",
    )
    grafico_barras(
        maior_faturamento.set_index("rotulo")["faturamento"],
        "Top 10 produtos por faturamento (pedidos entregues)",
        "Faturamento (R$)", "Produto (ID abreviado e categoria)",
        "top_produtos_faturamento", em_reais=True,
    )


# ==========================================
# 6. CATEGORIAS
# ==========================================

def analisar_categorias(base):
    titulo_secao("CATEGORIAS")

    por_categoria = base.groupby("product_category_name")["price"].agg(
        faturamento="sum", quantidade="size", media_por_item="mean"
    )

    top_faturamento = por_categoria["faturamento"].nlargest(10)
    top_quantidade = por_categoria["quantidade"].nlargest(10)
    top_media = por_categoria["media_por_item"].nlargest(10)

    print("10 categorias com maior faturamento:")
    for categoria, valor in top_faturamento.items():
        print(f"  {categoria}: {formatar_reais(valor)}")

    print("\n10 categorias com mais itens vendidos:")
    for categoria, valor in top_quantidade.items():
        print(f"  {categoria}: {formatar_inteiro(valor)} itens")

    print("\n10 categorias com maior preço médio por item:")
    for categoria, valor in top_media.items():
        print(f"  {categoria}: {formatar_reais(valor)}")

    grafico_barras(top_faturamento.rename(index=nome_bonito),
                   "Top 10 categorias por faturamento (pedidos entregues)",
                   "Faturamento (R$)", "Categoria", "categorias_faturamento", em_reais=True)
    grafico_barras(top_quantidade.rename(index=nome_bonito),
                   "Top 10 categorias por quantidade de itens vendidos",
                   "Quantidade de itens", "Categoria", "categorias_quantidade")
    grafico_barras(top_media.rename(index=nome_bonito),
                   "Top 10 categorias por preço médio do item",
                   "Preço médio (R$)", "Categoria", "categorias_preco_medio", em_reais=True)


# ==========================================
# 7. ESTADOS
# ==========================================

def analisar_estados(base, clientes):
    titulo_secao("ESTADOS")

    clientes_por_estado = clientes["customer_state"].value_counts().head(10)
    faturamento = base.groupby("customer_state")["price"].sum().nlargest(10)

    valor_por_pedido = base.groupby(["customer_state", "order_id"])["price"].sum()
    ticket_medio = valor_por_pedido.groupby("customer_state").mean().nlargest(10)

    print("10 estados com mais clientes:")
    print(clientes_por_estado)
    print("\n10 estados com maior faturamento (pedidos entregues):")
    print(faturamento.round(2))
    print("\n10 estados com maior valor médio por pedido:")
    print(ticket_medio.round(2))

    grafico_barras(clientes_por_estado, "Top 10 estados com mais clientes",
                   "Quantidade de clientes", "Estado", "estados_clientes")
    grafico_barras(faturamento, "Top 10 estados por faturamento (pedidos entregues)",
                   "Faturamento (R$)", "Estado", "estados_faturamento", em_reais=True)
    grafico_barras(ticket_medio, "Top 10 estados por valor médio do pedido",
                   "Valor médio por pedido (R$)", "Estado", "estados_ticket_medio", em_reais=True)


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    pedidos, itens, produtos, clientes = carregar_dados()
    base = montar_itens_entregues(pedidos, itens, produtos, clientes)

    verificar_qualidade(pedidos, clientes)
    analisar_periodo(pedidos)
    analisar_entregas(pedidos)
    analisar_faturamento_mensal(base, pedidos)
    analisar_produtos(base)
    analisar_categorias(base)
    analisar_estados(base, clientes)

    print(f"\nPronto! Gráficos salvos em: {PASTA_IMAGENS}")


if __name__ == "__main__":
    main()
