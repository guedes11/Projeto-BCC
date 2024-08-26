from extrai_tabelas import extrai_tabelas_da_url
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import pandas as pd
import re
    
                
urls = [
        f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ano}_-_Série_A" 
        for ano in range(2013, 2024)
       ]

extrai_tabelas_da_url(urls)

caminho = './Tabelas'

pontos_por_temporada = []
# Percorrendo a pasta Tabelas.
for arquivo in listdir(caminho):
    soma = 0

    # Lendo e transformando o arquivo .csv em Dataframe.
    arquivo_atual = pd.read_csv(caminho + '/' + arquivo)

    # Deletando as linhas e colunas irrelevantes.
    arquivo_atual = arquivo_atual.drop(axis=1, labels=["Unnamed: 0", "J", "V", "E", "D", "GP", "GC", "SG"])
    arquivo_atual = arquivo_atual.drop(axis=0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19])
    
    if "Classificação ou descenso" in arquivo_atual.columns:
        arquivo_atual.pop("Classificação ou descenso")
    else:
        arquivo_atual.pop("Unnamed: 10")
    
    # Removendo possiveis caracteres que não sejam numeros da coluna Pts, transformando em numeros e somando posteriormente
    arquivo_atual["Pts"] = arquivo_atual["Pts"].apply(lambda pontos: re.sub(r'\D', '', str(pontos)))
    arquivo_atual["Pts"] = pd.to_numeric(arquivo_atual["Pts"])
    soma = arquivo_atual["Pts"].sum()

    pontos_por_temporada.append(int(soma))

x = np.arange(start=2014, stop=2024)
y = pontos_por_temporada

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xticks(x)

plt.xlabel('Temporada')
plt.ylabel('Pontuação')
plt.title('Pontos do 1° time na zona de rebaixamento por Temporada.')
plt.grid(visible=True)
plt.show()
