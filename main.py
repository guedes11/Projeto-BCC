from io import StringIO
import openpyxl
import pandas as pd
import requests
import re


requisicao = requests.get("https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2023_-_S%C3%A9rie_A")
tabelas = pd.read_html(StringIO(requisicao.text))

dataframe = pd.DataFrame(tabelas[6])
dataframe.to_excel("TabelaJogos.xlsx", sheet_name='jogos_2023')

pasta_trabalho = openpyxl.load_workbook("TabelaJogos.xlsx")
planilha = pasta_trabalho.active
planilha.delete_cols(0)
planilha.delete_rows(0)

for linha in range(planilha.max_row):
    linha += 1
    for coluna in range(planilha.max_column):
        coluna += 1
        celula = planilha.cell(row=linha, column=coluna)

        if celula.value != "—" and coluna > 1:
            placar_final = map(int, re.findall(r'\d+', celula.value))
            gols = [gol for gol in placar_final]
            resultado = gols[0] - gols[1]

            if resultado > 0:
                celula.value = 3
            elif resultado == 0:
                celula.value = 1
            else:
                celula.value = 0
        
        print(celula.value, end='|')
    print()

pasta_trabalho.close()
pasta_trabalho.save("TabelaJogosAtualizada.xlsx")
