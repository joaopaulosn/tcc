import itertools
from pyvis.network import Network
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
# EXPORTAÇÃO 3: Grafo Interativo com PyVis (Maior Componente Conectada)
# -------------------------------------------------------------
largest_cc = max(nx.connected_components(G), key=len)
subG = G.subgraph(largest_cc)

net = Network(
    height="750px",
    width="100%",
    bgcolor="#ffffff",
    font_color="black",
    notebook=False,
)

top_15 = set(
    df_metrics.sort_values(by="Coautores Diretos", ascending=False).head(15)[
        "Autor"
    ]
)

for n in subG.nodes():
    gender = subG.nodes[n].get("gender", "Desconhecido")
    if gender == "Feminino":
        color = "#e377c2"
    elif gender == "Masculino":
        color = "#1f77b4"
    else:
        color = "gray"

    size = degree_dict[n] * 1.5 + 8
    label = n if n in top_15 else ""  # Exibe o nome apenas para os Top 15

    net.add_node(
        n,
        label=label,
        title=f"Autor: {n}\nGênero: {gender}\nCoautores: {degree_dict[n]}",
        color=color,
        size=size,
    )

for edge in subG.edges(data=True):
    net.add_edge(edge[0], edge[1], weight=edge[2].get("weight", 1), color="gray")

net.repulsion(
    node_distance=150, central_gravity=0.3, spring_length=200, spring_strength=0.05
)
net.save_graph("rede_coautoria_sbsc.html")
print("Arquivo 'rede_coautoria_sbsc.html' gerado com sucesso!")