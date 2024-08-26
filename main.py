from pandas import read_html, to_numeric, DataFrame
from requests import get
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import re


# Extrai a Tabela de Confrontos de cada Edição do Brasileirão de 2013 até 2023
def extrai_tabelas_da_url(links: list):
    lista_dataframe = []
    for link in links:
        requisicao = get(link)
        lista_tabelas = read_html(StringIO(requisicao.text))

        # Filtra a tabela de Confronto pela sua dimensão e transforma em um arquivo .xlsx
        for tabela in lista_tabelas:
            if tabela.shape == (20, 11):
                dataframe = DataFrame(tabela)
                lista_dataframe.append(dataframe)
    return lista_dataframe
                
urls = [
        f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ano}_-_Série_A" 
        for ano in range(2013, 2024)
       ]


pontos_por_temporada = []
vitorias_por_temporada = []

# Percorrendo a pasta Tabelas.
for arquivo in extrai_tabelas_da_url(urls):

    # Lendo e transformando o arquivo .csv em Dataframe.
    arquivo_atual = arquivo

    # Deletando as linhas e colunas irrelevantes.
    arquivo_atual = arquivo_atual.drop(axis=0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19])
    
    if "Classificação ou descenso" in arquivo_atual.columns:
        arquivo_atual.pop("Classificação ou descenso")
    else:
        arquivo_atual.pop("Unnamed: 10")
    
    # Removendo possiveis caracteres que não sejam numeros da coluna Pts, transformando em numeros e somando posteriormente
    arquivo_atual["Pts"] = arquivo_atual["Pts"].apply(lambda pontos: re.sub(r'\D', '', str(pontos)))
    arquivo_atual["Pts"] = to_numeric(arquivo_atual["Pts"])

    pontos_por_temporada.append(int(arquivo_atual["Pts"]))

    arquivo_atual["V"] = to_numeric(arquivo_atual["V"])
    vitorias_por_temporada.append(int(arquivo_atual["V"]))


num_elementos = (len(pontos_por_temporada) + len(vitorias_por_temporada)) / 2

media_pontos = sum(pontos_por_temporada) / num_elementos
media_vitorias = sum(vitorias_por_temporada) / num_elementos

variancia_pontos = sum([(valor - media_pontos)**2 for valor in pontos_por_temporada]) / num_elementos
variancia_vitorias = sum([(valor - media_vitorias)**2 for valor in vitorias_por_temporada]) / num_elementos

desvio_padrao_pontos = variancia_pontos ** 0.5
desvio_padrao_vitorias = variancia_vitorias ** 0.5

covariancia = sum([(vitorias_por_temporada[i] - media_vitorias) * (pontos_por_temporada[i] - media_pontos) for i in range(0, 10)]) / num_elementos

correlação = covariancia / (desvio_padrao_pontos * desvio_padrao_vitorias)

