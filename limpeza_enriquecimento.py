import pandas as pd

# 1. Carregar a sua base de dados existente
# (se for .xlsx, use pd.read_excel)
df = pd.read_csv('sbsc_dataset_enriquecido_ibge_2006_2025.csv')

# Lista de todas as colunas de afiliação da sua base
colunas_afiliacao = [
    'first-author-affiliation',
    'second-author-affiliation',
    'third-author-affiliation',
    'fourth-author-affiliation',
    'fifth-author-affiliation',
    'sixth-author-affiliation',
    'seventh-author-affiliation',
    'eighth-author-affiliation',
]

# Dicionário com os mapas das substituições que você solicitou
mapa_limpeza = {
    # PUC MG e variações
    'PUC/MG': 'PUC-MG',
    'PUCMG': 'PUC-MG',
    'PUC MG': 'PUC-MG',
    # PUCs de outros estados
    'PUC/RIO': 'PUC-Rio',
    'PUC-RJ': 'PUC-Rio',
    'PUC RIO': 'PUC-Rio',
    'PUC/PR': 'PUCPR',
    'PUC-PR': 'PUCPR',
    'PUC PR': 'PUCPR',
    'PUC/RS': 'PUCRS',
    'PUC-RS': 'PUCRS',
    'PUC RS': 'PUCRS',
    # UFPA
    'Universidade Federal do Pará': 'UFPA',
    'Universidade Federal do Para': 'UFPA',
    # USP
    'Universidade de São Paulo': 'USP',
    'Universidade de Sao Paulo': 'USP',
    # Feevale
    'Universidade Feevale': 'Feevale',
    'feevale': 'Feevale',
    # CEFETs
    'CEFET/RJ': 'CEFET-RJ',
    'CEFET RJ': 'CEFET-RJ',
    'CEFET/MG': 'CEFET-MG',
    'CEFET MG': 'CEFET-MG',

    #farroupilha

    'IFFarroupilha': 'IFFar',
}

# 2. Aplicar a limpeza em todas as colunas de afiliação
for col in colunas_afiliacao:
    if col in df.columns:
        df[col] = df[col].replace(mapa_limpeza)

# 3. Salvar o dataset atualizado
df.to_csv('sbsc_dataset_enriquecido_limpo.csv', index=False)

print('Limpeza concluída e arquivo salvo como "sbsc_dataset_enriquecido_limpo.csv"!')
