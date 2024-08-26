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
            if tabela.shape == (20, 11) or tabela.shape == (20, 12) or tabela.shape == (20, 13):
                dataframe = DataFrame(tabela)
                lista_dataframe.append(dataframe)
    return lista_dataframe
                
urls = [
        f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ano}_-_Série_A"
        for ano in range(2013, 2024)
       ]


pontos_por_temporada = []
vitorias_por_temporada = []

# Iterando sobre a lista de Dataframes
for arquivo in extrai_tabelas_da_url(urls):
    # Deletando as linhas e colunas irrelevantes.
    arquivo = arquivo.drop(axis=0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19])

    if "P" in arquivo.columns:
        arquivo = arquivo.rename(columns={"P": "Pts"})

    # Removendo possiveis caracteres que não sejam numeros da coluna Pts, transformando em numeros e somando posteriormente.
    arquivo["Pts"] = arquivo["Pts"].apply(lambda pontos: re.sub(r'\D', '', str(pontos)))
    arquivo["Pts"] = to_numeric(arquivo["Pts"])

    pontos = int(arquivo["Pts"].iloc[0])
    pontos_por_temporada.append(44 if pontos == 443 else pontos)

    arquivo["V"] = to_numeric(arquivo["V"])
    
    vitorias = int(arquivo["V"].iloc[0])
    vitorias_por_temporada.append(vitorias)

x_temporadas = [ano for ano in range(2013, 2024)]

# Criação do gráfico de pontos por temporada.
fig, ax = plt.subplots()
ax.plot(x_temporadas, pontos_por_temporada)
ax.set_xticks(x_temporadas)
ax.grid()

plt.xlabel("Temporada")
plt.ylabel("Pontuação final")
plt.title("Pontuação final do 17° colocado (2013-2023).")
plt.savefig("./Graficos/pontosXtemporada.png")
plt.show()

# Criação do gráfico de vitórias por temporada.
fig, ax = plt.subplots()
ax.plot(x_temporadas, vitorias_por_temporada)
ax.set_xticks(x_temporadas)
ax.grid()

plt.xlabel("Temporada")
plt.ylabel("Total vitórias")
plt.title("Total de vitórias do 17° colocado (2013-2023).")
plt.savefig("./Graficos/vitoriasXtemporada.png")
plt.show()

# Criação do gráfico de correlação de vitorias/pontos do 17° colocado.
plt.scatter(pontos_por_temporada, vitorias_por_temporada)
plt.xlabel("Pontos")
plt.ylabel("Vitórias")
plt.title("Correlação entre Vitórias e Pontos no Brasileirão (2013-2023)")

# Criação da linha de tendencia do gráfico de vitorias x pontos
z = np.polyfit(pontos_por_temporada, vitorias_por_temporada, 1)
p = np.poly1d(z)

plt.plot(pontos_por_temporada, p(pontos_por_temporada))
plt.savefig("./Graficos/correlacaoVitorias_Pontos.png")

plt.show()