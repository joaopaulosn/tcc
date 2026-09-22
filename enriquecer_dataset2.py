import time
import unicodedata
import pandas as pd
import requests

# 1. Cache global para evitar chamadas repetidas à API do IBGE
cache_ibge = {}


def normalizar_texto(texto):
    """Remove acentos, espaços extras e converte para maiúsculas."""
    if pd.isna(texto) or not str(texto).strip():
        return ''
    # Normalização NFKD para separar os acentos das letras
    nfkd = unicodedata.normalize('NFKD', str(texto))
    texto_sem_acento = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    return texto_sem_acento.strip().upper()


def consultar_genero_ibge(nome):
    """Consulta a API do IBGE comparando as frequências do sexo Masculino e Feminino."""
    if pd.isna(nome) or not str(nome).strip():
        return ''

    primeiro_nome = str(nome).strip().split()[0].lower()

    if primeiro_nome in cache_ibge:
        return cache_ibge[primeiro_nome]

    url_m = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{primeiro_nome}?sexo=M'
    url_f = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{primeiro_nome}?sexo=F'

    freq_m = 0
    freq_f = 0

    try:
        res_m = requests.get(url_m, timeout=5).json()
        if res_m and len(res_m) > 0 and 'res' in res_m[0]:
            freq_m = sum(item['frequencia'] for item in res_m[0]['res'])

        res_f = requests.get(url_f, timeout=5).json()
        if res_f and len(res_f) > 0 and 'res' in res_f[0]:
            freq_f = sum(item['frequencia'] for item in res_f[0]['res'])

        if freq_m > freq_f:
            genero = 'Masculino'
        elif freq_f > freq_m:
            genero = 'Feminino'
        else:
            genero = 'Indefinido'

    except Exception:
        genero = 'Indefinido'

    if genero == 'Indefinido':
        if primeiro_nome.endswith(('a', 'ine', 'is', 'ele', 'is')):
            genero = 'Feminino'
        elif primeiro_nome.endswith(('o', 'os', 'or', 'el', 'us')):
            genero = 'Masculino'

    time.sleep(0.05)
    cache_ibge[primeiro_nome] = genero
    return genero


# 2. Dicionário de Mapeamento de Instituições -> (UF, Região)
mapa_instituicoes = {
    # Sudeste
    'UFRJ': ('RJ', 'Sudeste'),
    'SEFAZ': ('RJ', 'Sudeste'),
    'ENSP': ('RJ', 'Sudeste'),
    'INSTITUTO DE PESQUISAS JARDIM BOTANICO DO RIO DE JANEIRO': ('RJ', 'Sudeste'),
    'UNIRIO': ('RJ', 'Sudeste'),
    'PUC-RIO': ('RJ', 'Sudeste'),
    'PUC-RJ': ('RJ', 'Sudeste'),
    'LNCC': ('RJ', 'Sudeste'),
    'UFF': ('RJ', 'Sudeste'),
    'UERJ': ('RJ', 'Sudeste'),
    'INES': ('RJ', 'Sudeste'),
    'IME': ('RJ', 'Sudeste'),
    'CEFET/RJ': ('RJ', 'Sudeste'),
    'CEFET-RJ': ('RJ', 'Sudeste'),
    'USP': ('SP', 'Sudeste'),
    'UNIVERSIDADE DE SAO PAULO': ('SP', 'Sudeste'),
    'UNISANTOS': ('SP', 'Sudeste'),
    'IFSP': ('SP', 'Sudeste'),
    'FATEC': ('SP', 'Sudeste'),
    'UNISO': ('SP', 'Sudeste'),
    'UNICAMP': ('SP', 'Sudeste'),
    'UNESP': ('SP', 'Sudeste'),
    'ITA': ('SP', 'Sudeste'),
    'UFSCAR': ('SP', 'Sudeste'),
    'UFABC': ('SP', 'Sudeste'),
    'UFMG': ('MG', 'Sudeste'),
    'UNIFAL': ('MG', 'Sudeste'),
    'UFU': ('MG', 'Sudeste'),
    'FESJF': ('MG', 'Sudeste'),
    'UNA': ('MG', 'Sudeste'),
    'PUCMG': ('MG', 'Sudeste'),
    'PUC-MG': ('MG', 'Sudeste'),
    'FIVJ': ('MG', 'Sudeste'),
    'UFSJ': ('MG', 'Sudeste'),
    'FACULDADE DE CIENCIAS MEDICAS DE MINAS GERAIS': ('MG', 'Sudeste'),
    'UFVJM': ('MG', 'Sudeste'),
    'UFJF': ('MG', 'Sudeste'),
    'CEFET-MG': ('MG', 'Sudeste'),
    'UNIFEI': ('MG', 'Sudeste'),
    'UFV': ('MG', 'Sudeste'),
    'UFLA': ('MG', 'Sudeste'),
    'UFOP': ('MG', 'Sudeste'),
    'UFES': ('ES', 'Sudeste'),
    'CENTRO UNIVERSITARIO VILA VELHA': ('ES', 'Sudeste'),
    'UP': ('SP', 'Sudeste'),
    'IFRJ': ('RJ', 'Sudeste'),
    'FIOCRUZ': ('RJ', 'Sudeste'),
    'IEN': ('RJ', 'Sudeste'),
    'IPT': ('SP', 'Sudeste'),
    'CENTRO PAULA SOUZA': ('SP', 'Sudeste'),
    'CPS': ('SP', 'Sudeste'),
    'UNIFESP': ('SP', 'Sudeste'),
    # Norte
    'UFAM': ('AM', 'Norte'),
    'INPA': ('AM', 'Norte'),
    'UFRA': ('AM', 'Norte'),
    'UEA': ('AM', 'Norte'),
    'UNINORTE': ('AM', 'Norte'),
    'IFAM': ('AM', 'Norte'),
    'UFPA': ('PA', 'Norte'),
    'UNIVERSIDADE FEDERAL DO PARA': ('PA', 'Norte'),
    'UFOPA': ('PA', 'Norte'),
    'IFPA': ('PA', 'Norte'),
    'UNIFAP': ('AP', 'Norte'),
    'UFRR': ('RR', 'Norte'),
    'UNIR': ('RO', 'Norte'),
    'SIDIA': ('AM', 'Norte'),
    # Nordeste
    'UFBA': ('BA', 'Nordeste'),
    'UNEB': ('BA', 'Nordeste'),
    'FACULDADE RUY BARBOSA': ('BA', 'Nordeste'),
    'UNIFACS': ('BA', 'Nordeste'),
    'UESB': ('BA', 'Nordeste'),
    'IFBAIANO': ('BA', 'Nordeste'),
    'IFBA': ('BA', 'Nordeste'),
    'UEFS': ('BA', 'Nordeste'),
    'UFPE': ('PE', 'Nordeste'),
    'UNIVASF': ('PE', 'Nordeste'),
    'IFPE': ('PE', 'Nordeste'),
    'EMPREL': ('PE', 'Nordeste'),
    'CESAR': ('PE', 'Nordeste'),
    'UFRPE': ('PE', 'Nordeste'),
    'UFC': ('CE', 'Nordeste'),
    'UECE': ('CE', 'Nordeste'),
    'IFCE': ('CE', 'Nordeste'),
    'UNIFOR': ('CE', 'Nordeste'),
    'UFRN': ('RN', 'Nordeste'),
    'IFRN': ('RN', 'Nordeste'),
    'UFPB': ('PB', 'Nordeste'),
    'UFCG': ('PB', 'Nordeste'),
    'UFMA': ('MA', 'Nordeste'),
    'IFMA': ('MA', 'Nordeste'),
    'UFPI': ('PI', 'Nordeste'),
    'UFAL': ('AL', 'Nordeste'),
    'UFS': ('SE', 'Nordeste'),
    'UPE': ('PE', 'Nordeste'),
    'UFRB': ('BA', 'Nordeste'),
    'IFPB': ('PB', 'Nordeste'),
    # Sul
    'UDESC': ('SC', 'Sul'),
    'IFSC': ('SC', 'Sul'),
    'UFSC': ('SC', 'Sul'),
    'FURB': ('SC', 'Sul'),
    'UNIVALI': ('SC', 'Sul'),
    'UTFPR': ('PR', 'Sul'),
    'UEM': ('PR', 'Sul'),
    'UEL': ('PR', 'Sul'),
    'UNICESUMAR': ('PR', 'Sul'),
    'TECPAR': ('PR', 'Sul'),
    'PUCPR': ('PR', 'Sul'),
    'PUC-PR': ('PR', 'Sul'),
    'UFPR': ('PR', 'Sul'),
    'UNIOESTE': ('PR', 'Sul'),
    'UFRGS': ('RS', 'Sul'),
    'PUCRS': ('RS', 'Sul'),
    'PUC-RS': ('RS', 'Sul'),
    'UPF': ('RS', 'Sul'),
    'IFSUL': ('RS', 'Sul'),
    'UNISINOS': ('RS', 'Sul'),
    'UFSM': ('RS', 'Sul'),
    'FEEVALE': ('RS', 'Sul'),
    'IFFAR': ('RS', 'Sul'),
    'URI': ('RS', 'Sul'),
    'UNIPAMPA': ('RS', 'Sul'),
    # Centro-Oeste
    'UNB': ('DF', 'Centro-Oeste'),
    'UFG': ('GO', 'Centro-Oeste'),
    'UFMS': ('MS', 'Centro-Oeste'),
    'UFMT': ('MT', 'Centro-Oeste'),
    'UFT': ('TO', 'Centro-Oeste'),
    'CENTRO UNIVERSITARIO LUTERANO DE PALMAS': ('TO', 'Centro-Oeste'),
}


def extrair_uf_regiao(filiacao):
    """Mapeia o texto da filiação para a respectiva UF e Região do Brasil, ignorando acentos e case."""
    filiacao_norm = normalizar_texto(filiacao)

    if not filiacao_norm:
        return '', ''

    # Busca por correspondência no dicionário
    for inst, (uf, reg) in mapa_instituicoes.items():
        inst_norm = normalizar_texto(inst)
        if inst_norm in filiacao_norm:
            return uf, reg

    return 'Outro/Internacional', 'Outro/Internacional'


# 3. Execução Principal: Processamento das abas do Excel
excel_file = 'Dataset SBSC 2006-2025 - Tratado.xlsx'
xls = pd.ExcelFile(excel_file)
lista_dfs = []

print('Iniciando o enriquecimento com a API de Nomes do IBGE...')

for sheet_name in xls.sheet_names:
    df_sheet = pd.read_excel(excel_file, sheet_name=sheet_name)
    df_sheet['Ano_Publicacao'] = sheet_name

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
        col_affil = f'{ordem}-author-affiliation'

        if col_nome in df_sheet.columns:
            df_sheet[f'{ordem}_author_gender'] = df_sheet[col_nome].apply(
                consultar_genero_ibge
            )

        if col_affil in df_sheet.columns:
            res = df_sheet[col_affil].apply(extrair_uf_regiao)
            df_sheet[f'{ordem}_author_uf'] = [r[0] for r in res]
            df_sheet[f'{ordem}_author_regiao'] = [r[1] for r in res]

    lista_dfs.append(df_sheet)
    print(f'Aba {sheet_name} processada com sucesso.')

df_consolidado = pd.concat(lista_dfs, ignore_index=True)

nome_arquivo_saida = 'sbsc_dataset_enriquecido_ibge_2006_2025.csv'
df_consolidado.to_csv(nome_arquivo_saida, index=False, encoding='utf-8-sig')

print(f'\nConcluído! Base gerada com {len(df_consolidado)} artigos.')
print(f'Arquivo salvo como: "{nome_arquivo_saida}"')