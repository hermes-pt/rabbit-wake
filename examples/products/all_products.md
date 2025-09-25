get
https://api.fbits.net/produtos


Query Params
pagina
int32
Página da lista (padrão: 1)

categorias
string
Lista de categorias que deverão retornar (lista separada por "," ex.: 1,2,3), caso vazio retornará todas as categorias

fabricantes
string
Lista de fabricantes que deverão retornar (lista separada por "," ex.: 1,2,3), caso vazio retornará todas as situações

centrosDistribuicao
string
Lista de centros de distribuição que deverão retornar (lista separada por "," ex.: 1,2,3), caso vazio retornará produtos de todos os cd's

alteradosPartirDe
date
Retorna apenas os produtos que sofreram alguma alteração a partir da data/hora informada. Formato: aaaa-mm-dd hh:mm:ss com no máximo 48 horas de antecedência

quantidadeRegistros
int32
Quantidade de registros que deverão retornar (max: 50)

somenteValidos
boolean
Retorna apenas os produtos que estão marcados como válido


camposAdicionais
array of strings
Campos adicionais que se selecionados retornaram junto com o produto, valores aceitos: Atacado, Estoque, Atributo , Informacao, TabelaPreco