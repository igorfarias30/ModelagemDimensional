select MUNICIPIO, 
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
									inner join dimtempo temp on bf.idDimTempo = temp.idDimTempo;
                                 