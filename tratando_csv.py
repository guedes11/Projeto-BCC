import csv
from datetime import datetime

# Leitura do arquivo csv
leitor = csv.reader(open("./campeonato-brasileiro-full.csv", "r", encoding='utf-8', newline='\r\n'))

# Gravando as linhas do arquivo em uma lista
brasileirao = [linha for linha in leitor]

# Criando um novo arquivo com os campos desejados
with open("./campeonato_brasileiro.csv", "w", encoding='utf-') as arquivo_csv:

    for index, linha in enumerate(brasileirao):

        # Se a linha for igual ao cabeçalho ou o Ano for maior ou igual a 2006, a linha é escrita no arquivo
        if index == 0 or datetime.strptime(linha[2][-4:], "%Y").year >= 2006:
            arquivo_csv.write(f'{linha[1]},{linha[2]},{linha[4]},{linha[5]},{linha[10]}\n')
