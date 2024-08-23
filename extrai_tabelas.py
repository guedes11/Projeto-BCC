from pandas import DataFrame, read_html
from requests import get
from io import StringIO

caminho = "./Tabelas"
# Extrai a Tabela de Confrontos de cada Edição do Brasileirão de 2013 até 2023
def extrai_tabelas_da_url(urls: list):
    for ano, url in enumerate(urls):
        requisicao = get(url)
        lista_tabelas = read_html(StringIO(requisicao.text))

        # Filtra a tabela de Confronto pela sua dimensão e transforma em um arquivo .xlsx
        for tabela in lista_tabelas:
            if tabela.shape == (20,21):
                dataframe = DataFrame(tabela)
                dataframe.to_excel(f"{caminho}/TabelaJogos{ano + 2013}.xlsx")
