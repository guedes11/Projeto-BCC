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

media_pontos = []
# Percorrendo cada arquivo .csv da pasta Tabelas.
for arquivo in listdir(caminho):
    soma = 0

    arquivo_atual = pd.read_csv(caminho + '/' + arquivo)
    arquivo_atual = arquivo_atual.drop(axis=1, labels=["Unnamed: 0", "J", "V", "E", "D", "GP", "GC", "SG"])
    arquivo_atual = arquivo_atual.drop(axis=0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19])
    

    if "Classificação ou descenso" in arquivo_atual.columns:
        arquivo_atual.pop("Classificação ou descenso")
    else:
        arquivo_atual.pop("Unnamed: 10")
    
    arquivo_atual["Pts"] = arquivo_atual["Pts"].apply(lambda pontos: re.sub(r'\D', '', str(pontos)))
    arquivo_atual["Pts"] = pd.to_numeric(arquivo_atual["Pts"])
    soma = arquivo_atual["Pts"].sum()
    media_pontos.append(int(soma))

x = np.arange(start=2014, stop=2024)

fig, ax = plt.subplots()
ax.plot(x, media_pontos)
ax.set_xticks(x)

plt.xlabel('Temporada')
plt.ylabel('Pontuação')
plt.title('Pontos do 1 Time na zona de rebaixamento por Temporada.')
plt.grid(visible=True)
plt.show()

print(media_pontos)
