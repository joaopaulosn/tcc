import pandas as pd

# 1. Carregar a base enriquecida
df = pd.read_csv('sbsc_dataset_enriquecido_ibge_2006_2025.csv')
df.columns = [c.strip() for c in df.columns]

# 2. Desmembrar o dataset para Formato Longo (1 linha por autoria)
registros = []

for idx, row in df.iterrows():
    ano = row.get('Ano_Publicacao', row.get('publish-date', 'Desconhecido'))
    titulo = row.get('title', '')

    for i in range(1, 9):
        ordem = [
            'first',
            'second',
            'third',
            'fourth',
            'fifth',
            'sixth',
            'seventh',
            'eighth',
        ][i - 1]
        col_nome = f'{ordem}-author-name'
        col_gender = f'{ordem}_author_gender'
        col_uf = f'{ordem}_author_uf'
        col_regiao = f'{ordem}_author_regiao'

        nome = (
            str(row[col_nome]).strip().title()
            if col_nome in row and pd.notna(row[col_nome])
            else None
        )

        if nome and len(nome) > 2:
            gender = (
                row[col_gender]
                if col_gender in row and pd.notna(row[col_gender])
                else 'Indefinido'
            )
            uf = (
                row[col_uf]
                if col_uf in row and pd.notna(row[col_uf])
                else 'Outro/Internacional'
            )
            regiao = (
                row[col_regiao]
                if col_regiao in row and pd.notna(row[col_regiao])
                else 'Outro/Internacional'
            )

            registros.append({
                'artigo_id': idx,
                'ano': ano,
                'titulo': titulo,
                'ordem_autoria': i,
                'is_primeira_autoria': (i == 1),
                'autor': nome,
                'genero': gender,
                'uf': uf,
                'regiao': regiao,
            })

df_long = pd.DataFrame(registros)

# Filtrar apenas regiões brasileiras
regioes_br = ['Sudeste', 'Nordeste', 'Sul', 'Norte', 'Centro-Oeste']
df_br = df_long[df_long['regiao'].isin(regioes_br)].copy()

# ---------------------------------------------------------
# METRICAS DE AUTORES ÚNICOS E PROPORÇÃO
# ---------------------------------------------------------
unicos = (
    df_br.groupby(['regiao', 'genero'])['autor']
    .nunique()
    .unstack(fill_value=0)
)
unicos['Total_Autores'] = (
    unicos['Feminino'] + unicos['Masculino'] + unicos.get('Indefinido', 0)
)
unicos['Pct_Feminino'] = (
    unicos['Feminino'] / unicos['Total_Autores'] * 100
).round(2)
unicos['Pct_Masculino'] = (
    unicos['Masculino'] / unicos['Total_Autores'] * 100
).round(2)

# ---------------------------------------------------------
# METRICAS DE PRODUTIVIDADE (MÉDIA DE ARTIGOS POR AUTOR)
# ---------------------------------------------------------
artigos_por_autor = (
    df_br.groupby(['regiao', 'genero', 'autor'])['artigo_id']
    .nunique()
    .reset_index()
)
produtividade = (
    artigos_por_autor.groupby(['regiao', 'genero'])['artigo_id']
    .mean()
    .unstack(fill_value=0)
    .round(2)
)

# ---------------------------------------------------------
# METRICAS DE LIDERANÇA (PRIMEIRA AUTORIA)
# ---------------------------------------------------------
primeiros = df_br[df_br['is_primeira_autoria']]
lideranca = (
    primeiros.groupby(['regiao', 'genero'])['artigo_id']
    .count()
    .unstack(fill_value=0)
)
lideranca_pct = (
    lideranca.div(lideranca.sum(axis=1), axis=0) * 100
).round(2)

# ---------------------------------------------------------
# TABELA FINAL CONSOLIDADA (HOMENS E MULHERES)
# ---------------------------------------------------------
relatorio_completo = pd.DataFrame({
    'Autores Únicos (Mulheres)': unicos['Feminino'],
    'Autores Únicos (Homens)': unicos['Masculino'],
    '% Autoras (Mulheres)': unicos['Pct_Feminino'],
    '% Autores (Homens)': unicos['Pct_Masculino'],
    'Média Artigos/Mulher': produtividade['Feminino'],
    'Média Artigos/Homem': produtividade['Masculino'],
    '% 1ª Autoria (Mulheres)': lideranca_pct['Feminino'],
    '% 1ª Autoria (Homens)': lideranca_pct['Masculino'],
})

print('====================================================================')
print('      RELATÓRIO COMPARATIVO COMPLETO POR GÊNERO E REGIÃO (SBSC)')
print('====================================================================')
print(relatorio_completo.to_string())

# Salvar relatório
relatorio_completo.to_csv(
    'relatorio_genero_regiao_completo.csv', encoding='utf-8-sig'
)
print(
    '\n[Sucesso] Relatório exportado para "relatorio_genero_regiao_completo.csv"'
)
