import pandas as pd

# 1. Carregar o dataset existente
df = pd.read_csv('sbsc_dataset_enriquecido_limpo.csv')

# 2. Mapeamento completo dos 89 registros (todos os nomes únicos listados previamente)
correcao_genero = {
    # Nomes Femininos
    'suelyn concentius': 'Feminino',
    'jacilane h. rabelo': 'Feminino',
    'jacilane rabelo': 'Feminino',
    'lynn alves': 'Feminino',
    'karen botelho': 'Feminino',
    'karen s. figueiredo': 'Feminino',
    'karen moreschi': 'Feminino',
    'rosiane freitas': 'Feminino',
    'noemi p. pinto': 'Feminino',
    'rayane santos': 'Feminino',
    'dhanielly p. r. lima': 'Feminino',
    'dhanielly lima': 'Feminino',
    'nayat sanchez-pi': 'Feminino',
    'ingrhid theodoro': 'Feminino',
    'narallynne araujo': 'Feminino',
    'parcilene f. brito': 'Feminino',
    'linnyer b. ruiz': 'Feminino',
    'sionise gomes': 'Feminino',
    'pernille bjorn': 'Feminino',
    'k. vega': 'Feminino',  # Katia Vega

    # Nomes Masculinos
    'cesar franca': 'Masculino',
    'ailton ribeiro': 'Masculino',
    'ricarth lima': 'Masculino',
    'edward c. souza': 'Masculino',
    'huandy c. camargo': 'Masculino',
    'welton p. l. felix': 'Masculino',
    'kevin l. santos': 'Masculino',
    'hussein khalil': 'Masculino',
    'williamson silva': 'Masculino',
    'martony d. silva': 'Masculino',
    'prasun dewan': 'Masculino',
    'hamadou saliah-hassane': 'Masculino',
    'rayol m. neto': 'Masculino',
    'ig i. bittencourt': 'Masculino',
    'cleyton v. c. magalhaes': 'Masculino',
    'cleyton slaviero': 'Masculino',
    'cleyton c. trindade': 'Masculino',
    'leif singer': 'Masculino',
    'jauvane c. oliveira': 'Masculino',
    'iury araujo': 'Masculino',
    'eudisley anjos': 'Masculino',
    'maison melotti': 'Masculino',
    'cesar a. tacla': 'Masculino',
    'cesar marcondes': 'Masculino',
    'lennon v. a. dias': 'Masculino',
    'methanias c. junior': 'Masculino',
    'lincoln brito': 'Masculino',
    'jacques wainer': 'Masculino',
    'adabriand furtado': 'Masculino',
    'nandamudi vijaykumar': 'Masculino',
    'jean-pierre courtiat': 'Masculino',
    'jaime s. sichman': 'Masculino',
    'clever r. g. farias': 'Masculino',
    'raoni kulesza': 'Masculino',
    'weverton cordeiro': 'Masculino',

    # Iniciais / Demais Casos Mapeados
    'c.d.m. berkenbrock': 'Masculino',  # Charleston D. M. Berkenbrock
    'c.m. hirata': 'Masculino',        # Celso M. Hirata
    'c.t. fernandes': 'Masculino',     # Clovis T. Fernandes
    'm.c. pichiliani': 'Masculino',    # Mauro C. Pichiliani
    'a.p.c. silva': 'Masculino',
    'a. pereira': 'Masculino',
    'g. robichez': 'Masculino',
    'k. j. a. serique': 'Masculino',
    'j. l. c. santos': 'Masculino',
    'f. s. costa': 'Masculino',
    'j. m. f. maia': 'Masculino'
}

# 3. Substituir no DataFrame em todas as posições de autor
posicoes = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']

substituicoes_feitas = 0

for ordem in posicoes:
    col_nome = f'{ordem}-author-name'
    col_gen = f'{ordem}_author_gender'
    
    if col_nome in df.columns and col_gen in df.columns:
        for nome_busca, genero_correto in correcao_genero.items():
            mask = (df[col_nome].astype(str).str.strip().str.lower() == nome_busca) & (df[col_gen] == 'Indefinido')
            substituicoes_feitas += mask.sum()
            df.loc[mask, col_gen] = genero_correto

# 4. Salvar o resultado final
output_file = 'sbsc_dataset_genero_completo.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Sucesso! Total de {substituicoes_feitas} registros corrigidos.")
print(f"Novo arquivo salvo como: '{output_file}'")
