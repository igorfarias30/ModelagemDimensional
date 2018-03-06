# Trabalho de Modelagem Dimensional e Design de Dashboards

Foram utilizados dados do governo federal para a execução do projeto, disponibilizados no portal da transparência. Optamos por utilizar os dados do Bolsa Família e ver os pagamentos através do ano de 2017. Entretanto, em um único mês, a leitura do arquivo ficou inviável para ser lido em máquinas pessoais, logo, utilizamos parte dos dados para alimentarem os *dashboards*. Para baixar os dados, [clique aqui](http://www.portaltransparencia.gov.br/downloads/mensal.asp?c=BolsaFamiliaFolhaPagamento#meses01).

### Modelo Dimensional

Para a criação do *Data Warehouse*, foi utilizado o SGBD MySQL.
>No diretório 'Data Warehouse', contém o script para criação do cubo, basta executar o script `BolsaFamilaDW.sql`, para gerar as dimensões e a fato.

### ETL
Com o DW criado, utilizamos a linguagem de programação Python, para ler o conjunto de dados em formato **.csv**, devido ao sua poderosa *package* de processamento de dados:`pandas`.

Para fazer a leitura de dados e carga é necessário que o driver do MySQL esteja instalado na máquina. Para instalar, abra o `cmd` e digite:

```shell
$: $ pip install PyMySQL
 ```
Clique [aqui](https://github.com/PyMySQL/PyMySQL) em caso de dúvidas.

Após a instalação do driver, temos que executar o script. Para executar digite o comando abaixo:
 >**Nota:** o comando abaixo só funcionará, caso você tenha baixado o dataset, descompactado e ter colocado numa pasta chamada Data no repositório.

```python
$: python etl.py 201701_BolsaFamiliaFolhaPagamento.csv
 ```

### Dashboard
No *dashboard*, utilizamos o **Power BI**, ferramenta self-service BI da Microsoft.
> Atenção: O PowerBI precisa do driver do MySQL para fazer ligação com o banco de dados, baixe [aqui](https://dev.mysql.com/downloads/connector/net/6.10.html) e instale na sua máquina.

Após a conexão estiver estabelicida, execute o comando abaixo para carregar os dados do DW:
```SQL
select
MUNICIPIO, 
Estado,
REGIAO,
UF,
NIS,
Nome,
FONTE,
ANO,
MES,
DIA,
VALOR_PARCELA
from FatBolsaFamilia bf inner join dimmunicipio mun on bf.idDimCidade = mun.idDimCidade
						inner join dimfavorecido fav on bf.idDimFavorecido = fav.idDimFavorecido
						inner join dimfuncao fun on bf.idDimFuncao = fun.idDimFuncao
						inner join dimfonte font on bf.idDimFonte = font.idDimFonte
						inner join dimtempo temp on bf.idDimTempo = temp.idDimTempo
```

O nosso dashboard ficou dessa forma:

![GitHub Logo](/image/bi.png)


###### About
Igor Farias & Mateus Mota
