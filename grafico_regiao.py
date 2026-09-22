import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuração visual dos gráficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 11})

# 1. Carregar o arquivo CSV
# Ajuste o parâmetro index_col se a primeira coluna (regiões) não tiver nome
df = pd.read_csv("relatorio_regional_vs_brasil.csv")

# Nome da coluna contendo as regiões (se for a primeira coluna)
col_regiao = df.columns[0]

# -------------------------------------------------------------
# GRÁFICO 1: Autores Únicos (Homens vs Mulheres)
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
ax1 = df.plot(
    x=col_regiao,
    y=["Autores Únicos (Mulheres)", "Autores Únicos (Homens)"],
    kind="bar",
    color=["#e377c2", "#1f77b4"],
    width=0.6,
    figsize=(10, 6),
)

plt.title(
    "Total de Autores Únicos por Região e Média Nacional",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.ylabel("Quantidade de Autores Únicos")
plt.xlabel("")
plt.xticks(rotation=15)
plt.legend(["Mulheres", "Homens"])

# Rótulos de dados sobre as barras
for p in ax1.patches:
    val = p.get_height()
    if val > 0:
        ax1.annotate(
            f"{int(val)}",
            (p.get_x() + p.get_width() / 2.0, val),
            ha="center",
            va="bottom",
            fontweight="bold",
            xytext=(0, 3),
            textcoords="offset points",
        )

plt.tight_layout()
plt.savefig("grafico_1_autores_unicos.png", dpi=300)
plt.show()

# -------------------------------------------------------------
# GRÁFICO 2: Percentual de Autores Homens e Mulheres (%)
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
ax2 = df.plot(
    x=col_regiao,
    y=["% Autoras (Mulheres)", "% Autores (Homens)"],
    kind="bar",
    stacked=True,
    color=["#e377c2", "#1f77b4"],
    width=0.55,
    figsize=(10, 6),
)

plt.title(
    "Percentual de Autores Únicos por Região e Média Nacional (%)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.ylabel("Porcentagem (%)")
plt.xlabel("")
plt.xticks(rotation=0)
plt.legend(
    ["Mulheres (%)", "Homens (%)"], bbox_to_anchor=(1.02, 1), loc="upper left"
)

# Rótulos dentro das barras empilhadas
for p in ax2.patches:
    val = p.get_height()
    if val > 5:
        ax2.text(
            p.get_x() + p.get_width() / 2,
            p.get_y() + val / 2,
            f"{val:.1f}%",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
        )

plt.tight_layout()
plt.savefig("grafico_2_percentual_autores.png", dpi=300)
plt.show()

# -------------------------------------------------------------
# GRÁFICO 3: Média de Artigos por Homem e Mulher
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
ax3 = df.plot(
    x=col_regiao,
    y=["Média Artigos/Mulher", "Média Artigos/Homem"],
    kind="bar",
    color=["#e377c2", "#1f77b4"],
    width=0.6,
    figsize=(10, 6),
)

plt.title(
    "Média de Artigos Publicados por Autor(a) por Região e Média Nacional",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.ylabel("Média de Artigos / Autor")
plt.xlabel("")
plt.xticks(rotation=0)
plt.legend(["Mulheres", "Homens"])

# Rótulos de dados sobre as barras
for p in ax3.patches:
    val = p.get_height()
    if val > 0:
        ax3.annotate(
            f"{val:.2f}",
            (p.get_x() + p.get_width() / 2.0, val),
            ha="center",
            va="bottom",
            fontweight="bold",
            xytext=(0, 3),
            textcoords="offset points",
        )

plt.tight_layout()
plt.savefig("grafico_3_media_artigos.png", dpi=300)
plt.show()

# -------------------------------------------------------------
# GRÁFICO 4: Percentual de Primeira Autoria por Homem e Mulher (%)
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
ax4 = df.plot(
    x=col_regiao,
    y=["% 1ª Autoria (Mulheres)", "% 1ª Autoria (Homens)"],
    kind="bar",
    stacked=True,
    color=["#e377c2", "#1f77b4"],
    width=0.55,
    figsize=(10, 6),
)

plt.title(
    "Percentual de Primeira Autoria por Região e Média Nacional (%)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.ylabel("Porcentagem (%)")
plt.xlabel("")
plt.xticks(rotation=0)
plt.legend(
    ["Primeira Autora (Mulher)", "Primeiro Autor (Homem)"],
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
)

# Rótulos dentro das barras empilhadas
for p in ax4.patches:
    val = p.get_height()
    if val > 5:
        ax4.text(
            p.get_x() + p.get_width() / 2,
            p.get_y() + val / 2,
            f"{val:.1f}%",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
        )

plt.tight_layout()
plt.savefig("grafico_4_primeira_autoria.png", dpi=300)
plt.show()
