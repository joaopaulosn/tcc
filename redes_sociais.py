import itertools
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# 1. Carregar dataset
df = pd.read_csv("sbsc_dataset_genero_completo.csv")

# 2. Construir o grafo da rede de coautoria
G = nx.Graph()
positions = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
]

for idx, row in df.iterrows():
    authors = []
    for pos in positions:
        col_name = f"{pos}-author-name"
        col_gen = f"{pos}_author_gender"

        if (
            col_name in df.columns
            and pd.notna(row[col_name])
            and str(row[col_name]).strip() != ""
        ):
            name = str(row[col_name]).strip().title()
            gen = (
                row[col_gen]
                if (col_gen in df.columns and pd.notna(row[col_gen]))
                else "Desconhecido"
            )
            authors.append(name)
            if name not in G:
                G.add_node(name, gender=gen)

    for a1, a2 in itertools.combinations(set(authors), 2):
        if G.has_edge(a1, a2):
            G[a1][a2]["weight"] += 1
        else:
            G.add_edge(a1, a2, weight=1)

# 3. Calcular métricas de centralidade
deg_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
degree_dict = dict(G.degree())

nodes_data = []
for node in G.nodes():
    nodes_data.append({
        "Autor": node,
        "Gênero": G.nodes[node].get("gender", "N/A"),
        "Coautores Diretos": degree_dict[node],
        "Centralidade Grau": round(deg_centrality[node], 6),
        "Intermediacao (Betweenness)": round(betweenness_centrality[node], 6),
        "Proximidade (Closeness)": round(closeness_centrality[node], 6),
    })

df_metrics = pd.DataFrame(nodes_data)
df_metrics.sort_values(by="Coautores Diretos", ascending=False, inplace=True)

# -------------------------------------------------------------
# EXPORTAÇÃO 1: Tabela completa em CSV
# -------------------------------------------------------------
df_metrics.to_csv(
    "metricas_centralidade_autores.csv", index=False, encoding="utf-8-sig"
)
print("Arquivo 'metricas_centralidade_autores.csv' gerado com sucesso!")

# -------------------------------------------------------------
# EXPORTAÇÃO 2: Relatório em TXT com Resumo e Rankings
# -------------------------------------------------------------
top_degree = df_metrics.sort_values(
    by="Coautores Diretos", ascending=False
).head(10)
top_betweenness = df_metrics.sort_values(
    by="Intermediacao (Betweenness)", ascending=False
).head(10)

with open("resumo_rede_coautoria.txt", "w", encoding="utf-8") as f:
    f.write("=== RESUMO GLOBAL DA REDE DE COAUTORIA SBSC ===\n")
    f.write(f"Total de Autores (Nos): {G.number_of_nodes()}\n")
    f.write(f"Total de Colaboracoes (Arestas): {G.number_of_edges()}\n")
    f.write(
        f"Numero de Componentes Conectados: {nx.number_connected_components(G)}\n\n"
    )

    f.write("=== TOP 10 - CENTRALIDADE DE GRAU ===\n")
    f.write(
        top_degree[[
            "Autor",
            "Gênero",
            "Coautores Diretos",
            "Centralidade Grau",
        ]].to_string(index=False)
    )

    f.write("\n\n=== TOP 10 - CENTRALIDADE DE INTERMEDIACAO ===\n")
    f.write(
        top_betweenness[[
            "Autor",
            "Gênero",
            "Intermediacao (Betweenness)",
        ]].to_string(index=False)
    )

print("Arquivo 'resumo_rede_coautoria.txt' gerado com sucesso!")

# -------------------------------------------------------------
# EXPORTAÇÃO 3: Imagem do Gráfico em PNG
# -------------------------------------------------------------
largest_cc = max(nx.connected_components(G), key=len)
subG = G.subgraph(largest_cc)

fig, ax = plt.subplots(figsize=(12, 10))
pos = nx.spring_layout(subG, k=0.15, seed=42)

colors = [
    (
        "#e377c2"
        if subG.nodes[n].get("gender") == "Feminino"
        else "#1f77b4" if subG.nodes[n].get("gender") == "Masculino" else "gray"
    )
    for n in subG.nodes()
]
sizes = [degree_dict[n] * 25 for n in subG.nodes()]

nx.draw_networkx_nodes(
    subG, pos, node_color=colors, node_size=sizes, alpha=0.85, ax=ax
)
nx.draw_networkx_edges(subG, pos, alpha=0.2, edge_color="gray", ax=ax)

top_15 = set(
    df_metrics.sort_values(by="Coautores Diretos", ascending=False).head(15)[
        "Autor"
    ]
)
labels = {n: n for n in subG.nodes() if n in top_15}
nx.draw_networkx_labels(
    subG, pos, labels=labels, font_size=8, font_weight="bold", ax=ax
)

plt.title(
    "Rede de Coautoria SBSC - Maior Componente Conectada",
    fontsize=13,
    fontweight="bold",
)
plt.axis("off")

pink_dot = mlines.Line2D(
    [],
    [],
    color="#e377c2",
    marker="o",
    linestyle="None",
    markersize=10,
    label="Mulheres",
)
blue_dot = mlines.Line2D(
    [],
    [],
    color="#1f77b4",
    marker="o",
    linestyle="None",
    markersize=10,
    label="Homens",
)
plt.legend(handles=[pink_dot, blue_dot], loc="lower right", fontsize=11)

plt.tight_layout()
plt.savefig("rede_coautoria_sbsc.png", dpi=300)
plt.show()