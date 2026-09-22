import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuração visual
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 11})

# 1. Carregar Dataset
df = pd.read_csv("sbsc_dataset_genero_completo.csv")

# Extrair exatamente os 4 dígitos do ano sem passar pelo pd.to_datetime()
year_col = "publish-date" if "publish-date" in df.columns else "ano"
df["ano"] = (
    df[year_col].astype(str).str.extract(r"(\d{4})")[0].astype(int)
)

print("Anos identificados no dataset:", sorted(df["ano"].unique()))

# 2. Estruturar participações individuais por ano
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
records = []

for idx, row in df.iterrows():
    yr = row["ano"]
    title = row.get("title", f"artigo_{idx}")

    for i, pos in enumerate(positions):
        col_name = f"{pos}-author-name"
        col_gen = f"{pos}_author_gender"
        col_reg = f"{pos}_author_regiao"

        if (
            col_name in df.columns
            and pd.notna(row[col_name])
            and str(row[col_name]).strip() != ""
        ):
            name = str(row[col_name]).strip().title()
            gen = (
                row[col_gen]
                if (col_gen in df.columns and pd.notna(row[col_gen]))
                else None
            )
            reg = (
                row[col_reg]
                if (col_reg in df.columns and pd.notna(row[col_reg]))
                else None
            )

            records.append({
                "ano": yr,
                "autor": name,
                "genero": gen,
                "regiao": reg,
                "titulo": title,
                "is_first": (i == 0),
            })

df_authors = pd.DataFrame(records)
df_valid = df_authors[
    df_authors["genero"].isin(["Masculino", "Feminino"])
].copy()

# 3. Métricas Anuais (Feminino vs Masculino)
yearly_stats = []

for yr, group in df_valid.groupby("ano"):
    tot_artigos = group["titulo"].nunique()
    tot_autores = group["autor"].nunique()

    fem_autores = group[group["genero"] == "Feminino"]["autor"].nunique()
    masc_autores = group[group["genero"] == "Masculino"]["autor"].nunique()

    pct_fem = (fem_autores / tot_autores * 100) if tot_autores > 0 else 0
    pct_masc = (masc_autores / tot_autores * 100) if tot_autores > 0 else 0

    first_group = group[group["is_first"]]
    tot_first = len(first_group)
    fem_first = len(first_group[first_group["genero"] == "Feminino"])
    masc_first = len(first_group[first_group["genero"] == "Masculino"])

    pct_fem_first = (fem_first / tot_first * 100) if tot_first > 0 else 0
    pct_masc_first = (masc_first / tot_first * 100) if tot_first > 0 else 0

    yearly_stats.append({
        "Ano": int(yr),
        "Total_Artigos": tot_artigos,
        "Total_Autores_Unicos": tot_autores,
        "Autores_Fem": fem_autores,
        "Autores_Masc": masc_autores,
        "Pct_Autores_Fem": round(pct_fem, 2),
        "Pct_Autores_Masc": round(pct_masc, 2),
        "Pct_Primeira_Autoria_Fem": round(pct_fem_first, 2),
        "Pct_Primeira_Autoria_Masc": round(pct_masc_first, 2),
    })

df_yearly = pd.DataFrame(yearly_stats).sort_values(by="Ano")

# -------------------------------------------------------------
# EXPORTAÇÕES DE DADOS (CSV)
# -------------------------------------------------------------
df_yearly.to_csv("historico_evolucao_sbsc.csv", index=False, encoding="utf-8-sig")

cols_resumo = [
    "Ano",
    "Total_Artigos",
    "Total_Autores_Unicos",
    "Pct_Autores_Fem",
    "Pct_Autores_Masc",
    "Pct_Primeira_Autoria_Fem",
    "Pct_Primeira_Autoria_Masc",
]
df_yearly[cols_resumo].to_csv(
    "resumo_historico_sbsc.csv", index=False, encoding="utf-8-sig"
)
print("CSVs 'historico_evolucao_sbsc.csv' e 'resumo_historico_sbsc.csv' gerados!")

# -------------------------------------------------------------
# GRÁFICO 1: Comparação de Evolução por Gênero
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(
    df_yearly["Ano"],
    df_yearly["Pct_Autores_Fem"],
    marker="o",
    color="#e377c2",
    linewidth=2.5,
    label="% Autoras (Mulheres)",
)
ax1.plot(
    df_yearly["Ano"],
    df_yearly["Pct_Autores_Masc"],
    marker="o",
    color="#1f77b4",
    linewidth=2.5,
    label="% Autores (Homens)",
)

ax1.plot(
    df_yearly["Ano"],
    df_yearly["Pct_Primeira_Autoria_Fem"],
    marker="s",
    linestyle="--",
    color="#d62728",
    linewidth=2,
    label="% 1ª Autora (Mulheres)",
)
ax1.plot(
    df_yearly["Ano"],
    df_yearly["Pct_Primeira_Autoria_Masc"],
    marker="s",
    linestyle="--",
    color="#2ca02c",
    linewidth=2,
    label="% 1º Autor (Homens)",
)

ax1.set_title(
    "Evolução Histórica da Participação por Gênero no SBSC",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
ax1.set_xlabel("Ano")
ax1.set_ylabel("Percentagem (%)")
ax1.set_xticks(df_yearly["Ano"])
plt.xticks(rotation=45)
ax1.set_ylim(0, 100)
ax1.legend(loc="center right", bbox_to_anchor=(1.25, 0.5))

plt.tight_layout()
plt.savefig("evolucao_historica_genero.png", dpi=300, bbox_inches="tight")
plt.show()

# -------------------------------------------------------------
# GRÁFICO 2: Volume de Artigos e Autores por Ano
# -------------------------------------------------------------
fig, ax2 = plt.subplots(figsize=(12, 6))

ax2.bar(
    df_yearly["Ano"] - 0.2,
    df_yearly["Total_Artigos"],
    width=0.4,
    label="Total de Artigos",
    color="#1f77b4",
)
ax2.bar(
    df_yearly["Ano"] + 0.2,
    df_yearly["Total_Autores_Unicos"],
    width=0.4,
    label="Total de Autores Únicos",
    color="#aec7e8",
)

ax2.set_title(
    "Crescimento de Publicações e Pesquisadores por Ano",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
ax2.set_xlabel("Ano")
ax2.set_ylabel("Quantidade")
ax2.set_xticks(df_yearly["Ano"])
plt.xticks(rotation=45)
ax2.legend(loc="upper left")

plt.tight_layout()
plt.savefig("evolucao_historica_volume.png", dpi=300)
plt.show()