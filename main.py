import pandas as pd

caminho = './campeonato_brasileiro.csv'
leitor = pd.read_csv(caminho)

caminho = caminho.replace("csv", "xlsx")

leitor.to_excel(caminho, index=None, header=True)

