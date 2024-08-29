from io import StringIO
from pandas import read_html, DataFrame
from numpy import polyfit, poly1d
from requests import get
import matplotlib.pyplot as plt


# cabeçalho de requisição
cabecalhos = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'
    }

# lista de urls
urls = [
    f"https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/tabelle/wettbewerb/BRA1?saison_id={ano}" for ano in range(2012, 2023)
    ]

# Extrai a Tabela Classificação de cada Edição do Brasileirão de 2013 até 2023
lista_dataframe = []
for link in urls:
    requisicao = get(link, headers=cabecalhos)
    lista_tabelas = read_html(StringIO(requisicao.text))

    # Percorrendo a lista_tabelas.
    for tabela in lista_tabelas:
        # filtrando a tabela pela sua dimensão.
        if tabela.shape == (20, 10):
            # convertendo a tabela em um Dataframe.
            dataframe = DataFrame(tabela)
            lista_dataframe.append(dataframe)


pontos_por_temporada = []
vitorias_por_temporada = []

# Iterando sobre a lista de Dataframes
for arquivo in lista_dataframe:

    # Selecionando o total de pontos e vitórias do 17° colocado.
    arquivo = arquivo.loc[16, ["Pts", "V"]]

    # Armazenando o total de pontos da temporada em uma lista
    pontos_por_temporada.append(arquivo["Pts"])
    
    # Armazenando o total de vitórias da temporada em uma lista
    vitorias_por_temporada.append(arquivo["V"])

x_temporadas = range(2013, 2024)

# Criação do gráfico de pontos por temporada.
fig, ax = plt.subplots()
ax.plot(x_temporadas, pontos_por_temporada)
ax.set_xticks(x_temporadas)
ax.grid()

plt.xlabel("Temporada")
plt.ylabel("Pontuação")
plt.title("Pontuação final do 17° colocado (2013-2023).")
plt.savefig("./Graficos/pontosXtemporada.png")
plt.show()

# Criação do gráfico de vitórias por temporada.
fig, ax = plt.subplots()
ax.plot(x_temporadas, vitorias_por_temporada)
ax.set_xticks(x_temporadas)
ax.grid()

plt.xlabel("Temporada")
plt.ylabel("Vitórias")
plt.title("Total de vitórias do 17° colocado (2013-2023).")
plt.savefig("./Graficos/vitoriasXtemporada.png")
plt.show()

# Criação do gráfico de correlação de vitorias/pontos do 17° colocado.
plt.scatter(vitorias_por_temporada, pontos_por_temporada)
plt.xlabel("Vitórias")
plt.ylabel("Pontos")
plt.title("Correlação entre Vitórias e Pontos no Brasileirão (2013-2023)")

# Criação da linha de tendencia do gráfico de vitorias x pontos
coeficientes = polyfit(vitorias_por_temporada, pontos_por_temporada, 1)
polinomio = poly1d(coeficientes)

plt.plot(vitorias_por_temporada, polinomio(vitorias_por_temporada), 'g-')
plt.savefig("./Graficos/correlacaoVitorias_Pontos.png")
plt.show()
