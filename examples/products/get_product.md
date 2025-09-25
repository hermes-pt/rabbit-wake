Retorna um produto buscando pelo seu identificador
get
https://api.fbits.net/produtos/{identificador}
Método responsável por retornar um produto específico buscando pelo seu identificador, que pode ser um sku ou produto variante. O tipo do identificador pode ser definido no campo tipoIdentificador. Também é possível informar quais informações adicionais devem ser retornadas na consulta utilizando o campo campos adicionais.

Log in to see full request history
time	status	user agent	
now	
200
now	
200
2h ago	
200
44 Requests This Month

Path Params
identificador
string
required
Valor único utilizado para identificar o produto

137509
Query Params
tipoIdentificador
string
Define se o identificador informado é um sku ou um id interno


Sku
camposAdicionais
array of strings
Campo opcional que define quais dados extras devem ser retornados em conjunto com os dados básicos do produto, valores aceitos: Atacado, Estoque, Atributo , Informacao, TabelaPreco


string

atributo
