from io import StringIO
import openpyxl
import pandas as pd
import requests
import re


# Extrai a Tabela de Confrontos de cada Edição do Brasileirão de 2013 até 2023
def extrai_tabelas_da_url(url: list):
    for ano, url in enumerate(urls):
        requisicao = requests.get(url)
        lista_tabelas = pd.read_html(StringIO(requisicao.text))

        # Filtra a tabela de Confronto pela sua dimensão e transforma em um arquivo .xlsx
        for tabela in lista_tabelas:
            if tabela.shape == (20,21):
                dataframe = pd.DataFrame(tabela)
                dataframe.to_excel(f".\Tabelas\TabelaJogos{ano + 2013}.xlsx")


urls = [
        f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ano}_-_Série_A" 
        for ano in range(2013, 2024)
       ]

extrai_tabelas_da_url(urls)

pasta_trabalho = openpyxl.load_workbook("TabelaJogos.xlsx")
planilha = pasta_trabalho.active
planilha.delete_cols(0)
planilha.delete_rows(0)

for linha in planilha.iter_rows(min_col=1):
    for campo in linha:
        celula = campo.value
        if celula != "—" and campo.col_idx > 1:
            gols_mandante, gols_visitante = placar = map(int, re.findall(r'\d+', celula))
            resultado = gols_mandante - gols_visitante

            celula = 3 if resultado > 0 else 1 if resultado == 0 else 0
        
        print(celula, end='|')
    print()

pasta_trabalho.close()
pasta_trabalho.save("TabelaJogosAtualizada.xlsx")
