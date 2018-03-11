# -*- coding: utf-8 -*-

# Modelagem Dimensional
# Igor Farias
# Mateus

def processing_data(data, number = 100000):
    #data -> 'Data/201701_BolsaFamiliaFolhaPagamento.csv'

    if not os.path.isfile(data):
        print("Dataset not found. Please, add dataset to Data folder")
        exit()

    # reading just 100000 rows the dataframe
    df = pd.read_csv(data, error_bad_lines=False, encoding = "ISO-8859-1", sep='\t', nrows=int(number))

    df['Regiao'] = None
    # add region name to dataframe
    def regiao(estado):
        if estado in ['MA','PI','CE','RN','PE','PB','SE','AL','BA']:
            return 'Nordeste'
        elif estado in ['AM', 'RR', 'RO', 'AP', 'TO', 'RO', 'AC']:
            return 'Norte'
        elif estado in ['MT', 'MS', 'GO', 'DF']:
            return 'Centro-Oeste'
        elif estado in ['SP', 'RJ', 'ES', 'MG']:
            return 'Sudeste'
        else:
            return 'Sul'

    # returning state's name to datafrane
    def estado(uf):
        if uf == 'MA':
            return 'Maranhão'
        elif uf == 'PI':
            return 'Piauí'
        elif uf == 'CE':
            return 'Ceará'
        elif uf == 'BA':
            return 'Bahia'
        elif uf == 'AL':
            return 'Alagoas'
        elif uf == 'SE':
            return 'Sergipe'
        elif uf == 'RN':
            return 'Rio Grande do Norte'
        elif uf == 'PE':
            return 'Pernambuco'
        elif uf == 'PB':
            return 'Paraíba'
        elif uf == 'AM':
            return 'Amazonas'
        elif uf == 'RR':
            return 'Roraima'
        elif uf == 'AP':
            return 'Amapá'
        elif uf == 'PA':
            return 'Pará'
        elif uf == 'TO':
            return 'Tocantins'
        elif uf == 'RO':
            return 'Rondonia'
        elif uf == 'AC':
            return 'Acre'
        elif uf == 'MT':
            return 'Mato Grosso'
        elif uf == 'MS':
            return 'Mato Grosso do Sul'
        elif uf == 'GO':
            return 'Goiás'
        elif uf == 'SP':
            return 'São Paulo'
        elif uf == 'RJ':
            return 'Rio de Janeiro'
        elif uf == 'ES':
            return 'Espirito Santo'
        elif uf == 'MG':
            return 'Minas Gerais'
        elif uf == 'PR':
            return 'Paraná'
        elif uf == 'RS':
            return 'Rio Grande do Sul'
        elif uf == 'SC':
            return 'Santa Catarina'
        elif uf == 'DF':
            return 'Distrito Federal'
        else:
            return ''

    # Adding Region and State to dataframe
    df['Regiao'] = df['UF'].apply(regiao)
    df['Estado'] = df['UF'].apply(estado)

    # I have to add a Fonte and Finalidade column and drop 'Fonte-Finalidade'
    df['Fonte'] = df['Fonte-Finalidade'].apply(lambda x: x.split('-')[0])
    df['Finalidade'] = df['Fonte-Finalidade'].apply(lambda x: x.split('-')[1])
    df.drop('Fonte-Finalidade', axis=1, inplace = True)

    # 'VALOR_PARCELA' is object, i have to remove char ',' and convert to float
    df['Valor Parcela'] = df['Valor Parcela'].apply(lambda num: float(num.replace(',', '')) if ',' in num else float(num))

    # return the datasets
    return df

# loading data to database
def load_data_dimension(dataset):
    # Connect to the database
    connection = pymysql.connect(host='localhost', user='root', password='', db='BolsaFamilaDW', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Adding data to DimMunicipio
            for cod_siafi in dataset['Código SIAFI Município'].unique():
                # Create a new record
                dataset_aux = dataset[dataset['Código SIAFI Município'] == cod_siafi]

                cidade = dataset_aux['Nome Município'].unique()[0]
                estado = dataset_aux['Estado'].unique()[0]
                regiao = dataset_aux['Regiao'].unique()[0]
                uf = dataset_aux['UF'].unique()[0]
                sql = """INSERT INTO DimMunicipio (COD_SIAFI, MUNICIPIO, ESTADO, REGIAO, UF) VALUES (%d, "%s", "%s", "%s", "%s")""" %(int(cod_siafi), cidade, estado, regiao, uf)
                cursor.execute(sql)#, ('webmaster@python.org', 'very-secret'))

            # adding data to DimFavorecido
            for nis in dataset['NIS Favorecido'].unique():
                dataset_aux = dataset[dataset['NIS Favorecido'] == nis]

                nome = dataset_aux['Nome Favorecido'].unique()[0]
                sql = """INSERT INTO DimFavorecido(NIS, NOME) VALUES ("{}", "{}")""".format(nis, nome)
                cursor.execute(sql)

            # adding data to DimFuncao
            for funcao in dataset['Código Função'].unique():
                dataset_aux = dataset[dataset['Código Função'] == funcao]

                subfuncao = dataset_aux['Código Subfunção'].unique()[0]
                acao = dataset_aux['Código Ação'].unique()[0]

                sql = """INSERT INTO DimFuncao(COD_FUNCAO, COD_SUBFUNCAO, COD_ACAO) VALUES({}, {}, {})""".format(funcao, subfuncao, acao)
                cursor.execute(sql)

            # add Data to DimFonte
            for fonte in dataset['Fonte'].unique():
                dataset_aux = dataset[dataset['Fonte'] == fonte]

                finalidade = dataset_aux['Finalidade'].unique()[0]
                sql = """INSERT INTO DimFonte(FONTE, FINALIDADE) VALUES("{}", "{}")""".format(fonte, finalidade)
                cursor.execute(sql)

            #add Data to DimTempo
            for data in dataset['Mês Competência'].unique():
                mes, ano = data.split('/')
                # the data hasn't
                sql = """INSERT INTO DimTempo(ANO, MES, DIA) VALUES({}, {}, 28)""".format(ano, mes)
                cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()

# load data to fact
def load_data_fact(dataset):
    # Connect to the database
    connection = pymysql.connect(host='localhost', user='root', password='', db='BolsaFamilaDW', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # reading all row
            for i in range(dataset.shape[0]):
                #idDimMunicipio
                municipio = """SELECT idDimCidade from DimMunicipio where MUNICIPIO = "{}" AND ESTADO = "{}" LIMIT 1""".format(dataset['Nome Município'][i], dataset['Estado'][i])
                cursor.execute(municipio)
                municipio = cursor.fetchone()

                #idDimTempo
                mes, ano = df['Mês Competência'][i].split('/')
                tempo = """SELECT idDimTempo from DimTempo where  MES = {} and ANO = {} LIMIT 1 """.format(int(mes), int(ano))
                cursor.execute(tempo)
                tempo = cursor.fetchone()

                #idDimFonte
                fonte = """SELECT idDimFonte FROM DimFonte where FONTE = "{}" and FINALIDADE = "{}" """.format(dataset['Fonte'][i], dataset['Finalidade'][i])
                cursor.execute(fonte)
                fonte = cursor.fetchone()

                #idDimFavorecido
                favorecido = """SELECT idDimFavorecido FROM DimFavorecido where NIS = '{}' """.format(dataset['NIS Favorecido'][i])
                cursor.execute(favorecido)
                favorecido = cursor.fetchone()

                #idDimFuncao
                funcao = """SELECT idDimFuncao FROM DimFuncao where COD_FUNCAO = {} """.format(dataset['Código Função'][i])
                cursor.execute(funcao)
                funcao = cursor.fetchone()

                # loading data to fact table
                insert = """INSERT INTO FatBolsaFamilia (idDimCidade, idDimFavorecido, idDimFuncao, idDimFonte, idDimTempo, VALOR_PARCELA) VALUES (%d, %d, %d, %d, %d, %.2f)"""%(municipio['idDimCidade'], favorecido['idDimFavorecido'], funcao['idDimFuncao'], fonte['idDimFonte'], tempo['idDimTempo'], float(dataset['Valor Parcela'][i]))
                cursor.execute(insert)

        # commit data
        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    import pandas as pd
    import sys
    import os

    try:
        import pymysql.cursors
    except ImportError:
        print("missing 'pymysql'. Type 'pip install PyMySQL' to install package")
        exit()

    if len(sys.argv) < 2:
        print("Missing a parameter in command line")
        print("Try: python etl.py <file> <number_lines>")
        exit()

    df = processing_data("Data/{}".format(sys.argv[1]), sys.argv[2])
    load_data_dimension(df)
    load_data_fact(df)
