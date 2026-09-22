import pandas as pd

# 1. Carregar a base enriquecida
df = pd.read_csv('sbsc_dataset_genero_completo.csv')
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


def calcular_metricas(df_subset):
    # Autores únicos por gênero
    unicos = df_subset.groupby('genero')['autor'].nunique()
    f_unicos = unicos.get('Feminino', 0)
    m_unicos = unicos.get('Masculino', 0)
    total_unicos = f_unicos + m_unicos + unicos.get('Indefinido', 0)

    pct_f = (f_unicos / total_unicos * 100) if total_unicos > 0 else 0
    pct_m = (m_unicos / total_unicos * 100) if total_unicos > 0 else 0

    # Produtividade Média (artigos por autor)
    art_por_autor = (
        df_subset.groupby(['genero', 'autor'])['artigo_id']
        .nunique()
        .reset_index()
    )
    prod_f = (
        art_por_autor[art_por_autor['genero'] == 'Feminino']['artigo_id'].mean()
        if f_unicos > 0
        else 0
    )
    prod_m = (
        art_por_autor[art_por_autor['genero'] == 'Masculino'][
            'artigo_id'
        ].mean()
        if m_unicos > 0
        else 0
    )

    # Liderança (% 1ª Autoria)
    primeiros = df_subset[df_subset['is_primeira_autoria']]
    lid_counts = primeiros['genero'].value_counts()
    lid_total = lid_counts.sum()
    lid_pct_f = (
        (lid_counts.get('Feminino', 0) / lid_total * 100) if lid_total > 0 else 0
    )
    lid_pct_m = (
        (lid_counts.get('Masculino', 0) / lid_total * 100)
        if lid_total > 0
        else 0
    )

    return {
        'Autores Únicos (Mulheres)': f_unicos,
        'Autores Únicos (Homens)': m_unicos,
        '% Autoras (Mulheres)': round(pct_f, 2),
        '% Autores (Homens)': round(pct_m, 2),
        'Média Artigos/Mulher': round(prod_f, 2),
        'Média Artigos/Homem': round(prod_m, 2),
        '% 1ª Autoria (Mulheres)': round(lid_pct_f, 2),
        '% 1ª Autoria (Homens)': round(lid_pct_m, 2),
    }


# 1. Calcular por Região
resultados = {}
for reg in regioes_br:
    df_reg = df_br[df_br['regiao'] == reg]
    resultados[reg] = calcular_metricas(df_reg)

# 2. Calcular Média Nacional Brasil
resultados['MÉDIA NACIONAL (BRASIL)'] = calcular_metricas(df_br)

relatorio_com_brasil = pd.DataFrame(resultados).T

print('====================================================================')
print('      RELATÓRIO REGIONAL VS. MÉDIA NACIONAL BRASIL (SBSC)')
print('====================================================================')
print(relatorio_com_brasil.to_string())

# Exportar arquivo CSV final
relatorio_com_brasil.to_csv(
    'relatorio_regional_vs_brasil.csv', encoding='utf-8-sig'
)
print(
    '\n[Sucesso] Tabela exportada para "relatorio_regional_vs_brasil.csv"'
)
