Limite de Requisições
Suggest Edits
A API possui uma política de acesso para garantir o bom desempenho da aplicação e não prejudicar o lojista. Nessa política definimos a quantidade de requisições que podem ser realizadas em um determinado período. Isso evita a instabilidade da API e garante a sua disponibilidade.

📘
Atenção:

Informamos que é extremamente importante manter o endereço de e-mail do responsável técnico cadastrado no token, pois notificações sobre a integração e alterações na API sempre serão enviadas para esse e-mail.

A API possui um limite de 120 requisições por minuto. Esse limite é por grupo de endpoint, ou seja, é possível realizar 120 requisições nos endpoints de Pedido, por exemplo, e outras 120 requisições nos endpoints de Produtos no mesmo minuto, porém quando ultrapassado esse limite resultará em uma mensagem de erro.

Veja abaixo dois exemplos, um sendo com retorno de sucesso e outro com erro.

Exemplo de código de retorno de sucesso (200):



Exemplo de retorno quando o limite por minuto for atingido, neste observe que retornamos o tempo em segundos que o integrador deve aguardar para realizar a próxima requisição, esse tempo está descrito no campo Retry-After:



Tratar essa informação na integração é importante para evitar o bloqueio de 1 hora do token, regra essa que será executada se houver 5 requisições com o limite esgotado, sendo de suma importância que o ERP ou responsável técnico pela integração sejam notificados desse bloqueio.

Boas práticas de utilização
A API dispõe de alguns endpoints de atualização em lote de 50 produtos, sendo essa uma boa prática para as atualizações que ocorrem com mais frequência no site do cliente como preço e estoque, possibilitando assim uma quantidade maior de SKUs atualizados por minuto.

Se seus produtos sofrem uma grande quantidade de alteração de estoque e/ou preço, sugerimos a implementação dessas atualizações em lote, garantindo a informação atualizada no site a todo momento.

Saiba mais sobre atualizações em lote acessando os artigos Estoque e Preço.

Confira abaixo alguns exemplos de requisições:

A API dispõe de alguns endpoints de atualização em lote de 50 produtos, sendo essa uma boa prática para as atualizações que ocorrem com mais frequência no site do cliente como preço e estoque, possibilitando assim uma quantidade maior de SKUs atualizados por minuto.

Se seus produtos sofrem uma grande quantidade de alteração de estoque e/ou preço, sugerimos a implementação dessas atualizações em lote, garantindo a informação atualizada no site a todo momento.

Saiba mais sobre atualizações em lote acessando os artigos Estoque e Preço.

Confira abaixo alguns exemplos de requisições:

Realizando uma atualização em lote de 50 produtos para preço ou estoque
1 Requisição - atualiza 50 produtos;
120 Requisições por minuto - atualiza 6K (mil) produtos por minuto;
120 requisições por minuto a cada 1 hora- atualiza 360k (mil) produtos por hora.

O Cadastro de Produtos utiliza mais de um endpoint para criação, diminuindo a quantidade por minuto, mas sabemos que a principal carga de criação de produto é na implantação do site, quando todos os produtos da loja estão sendo inseridos, então com o processo alinhado é possível realizar a carga com tempo durante essa etapa.

1 Requisição - atualiza 50 produtos;
120 Requisições por minuto - atualiza 6K (mil) produtos por minuto;
120 requisições por minuto a cada 1 hora- atualiza 360k (mil) produtos por hora.

O Cadastro de Produtos utiliza mais de um endpoint para criação, diminuindo a quantidade por minuto, mas sabemos que a principal carga de criação de produto é na implantação do site, quando todos os produtos da loja estão sendo inseridos, então com o processo alinhado é possível realizar a carga com tempo durante essa etapa.

Cadastro de 1 produto utilizando 4 endpoints no Grupo de Produto (limite de 120 requisições)
4 Requisições - cria 1 produto;
4 Requisições por minuto - cria 30 produtos por minuto;
4 requisições por minuto a cada 1 hora - cria 1800 (mil) produtos por hora.

4 Requisições - cria 1 produto;
4 Requisições por minuto - cria 30 produtos por minuto;
4 requisições por minuto a cada 1 hora - cria 1800 (mil) produtos por hora.