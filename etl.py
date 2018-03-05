# -*- coding: utf-8 -*-

def processing_data(data):
    # reading just 100000 rows the dataframe
    df = pd.read_csv('Data/201701_BolsaFamiliaFolhaPagamento.csv', error_bad_lines=False, encoding = "ISO-8859-1", sep='\t', nrows=100000)

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
        else:
            return ''

    # Adding Region and State to dataframe
    df['Regiao'] = df['UF'].apply(regiao)
    df['Estado'] = df['UF'].apply(estado)

    # I have to add a Fonte and Finalidade column and drop 'Fonte-Finalidade'
    df['Fonte'] = df['Fonte-Finalidade'].apply(lambda x: x.split('-')[0])
    df['Finalidade'] = df['Fonte-Finalidade'].apply(lambda x: x.split('-')[1])
    df.drop('Fonte-Finalidade', axis=1, inplace = True)

    #df.to_csv('Data\\Bolsa_Familia.csv', sep=';')

    # return the datasets
    return df

def load_data(dataset):
    # Connect to the database
    connection = pymysql.connect(host='localhost', user='root', password='', db='BolsaFamilaDW', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    SQL = ''
    try:
        with connection.cursor() as cursor:

            # DimMunicipio
            for cidade in dataset['Nome Município'].unique():
                # Create a new record
                dataset_aux = dataset[dataset['Nome Município'] == cidade]

                cod_siafi = dataset_aux['Código SIAFI Município'].unique()[0]
                estado = dataset_aux['Estado'].unique()[0]
                regiao = dataset_aux['Regiao'].unique()[0]
                uf = dataset_aux['UF'].unique()[0]
                sql = """INSERT INTO DimMunicipio (COD_SIAFI, MUNICIPIO, ESTADO, REGIAO, UF) VALUES (%d, "%s", "%s", "%s", "%s")""" %(int(cod_siafi), cidade, estado, regiao, uf) #.format(int(cod_siafi), cidade, estado, regiao, uf)
                #print(sql)
                #break
                SQL = sql
                cursor.execute(sql)#, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except:
        print(SQL)
    finally:
        connection.close()

if __name__ == '__main__':
    import pandas as pd
    import sys
    import os

    try:
        import pymysql.cursors
    except ImportError:
        print("missing 'pymysql'. Type 'pip install pymysql' to install package")
        exit()

    if len(sys.argv) < 1:
        print("Missing a parameter in command line")
        exit()

    df = processing_data("Data/{}".format(sys.argv[1]))
    load_data(df)