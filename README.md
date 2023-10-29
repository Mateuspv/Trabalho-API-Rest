# Trabalho-API-Rest
Trabalho de desenvolvimento web sobre API Rest
Ocorreu alguns Problemas na hora de enviar pull request para a branch main, e não conseguimos enviar o pull request, mas caso queira ver oq cada um fez é so ver as branchs separadas de cada pesso que está até que parte cada um fez

# Registrar Veículo
Método: POST /registrar_veiculo
Corpo Espera um objeto JSON no corpo da requisição com os dados do veículo a ser registrado. Os dados devem seguir o modelo RegistroVeiculo, que deve incluir campos como marca_veiculo, placa, cliente_nome, mecanico_nome, horario_chegada, etc.
Funcionamento: Esta API permite registrar um novo veículo que chega para manutenção. Ela atribui um ID único ao veículo, verifica se o veículo já está em manutenção e se um registro idêntico já existe. Se não houver horário de chegada fornecido, ele é preenchido com o horário atual. O registro é adicionado à lista de registros e uma mensagem de sucesso é retornada.

# Listar Registros 
Método: GET /registros
Parâmetros de Consulta (Query Parameters): Aceita vários parâmetros de consulta para filtrar os registros. Você pode fornecer um ou mais parâmetros, como id, marca_veiculo, placa, cliente_nome, mecanico_nome, horario_chegada, horario_saida. Os parâmetros são usados para filtrar a lista de registros.
Funcionamento: Esta API permite listar os registros de veículos com base nos parâmetros fornecidos. Ela filtra os registros de acordo com os parâmetros especificados e retorna os registros que correspondem aos critérios de consulta.

# Atualizar Registro
Método: PATCH /atualizar_registro/{id}
Parâmetros na URL: Requer o ID do registro que você deseja atualizar. Deve ser fornecido na URL.
Corpo: Aceita um objeto JSON no corpo da requisição com um campo horario_saida, que é opcional. Se você desejar atualizar o horário de saída, forneça-o no corpo da requisição.
Funcionamento: Esta API permite atualizar o registro de um veículo. Ela encontra o registro com base no ID fornecido, verifica se o registro existe, e então atualiza o horário de saída (ou usa o horário atual se fornecido). O registro atualizado é retornado como resposta.

# Excluir Registro
Método: DELETE /excluir_registro/{id}
Parâmetros na URL: Requer o ID do registro que você deseja excluir. Deve ser fornecido na URL.
Funcionamento: Esta API permite excluir o registro de um veículo. Ela encontra o registro com base no ID fornecido, verifica se o registro existe e se possui horário de saída. Se o registro não possui horário de saída, ele é excluído e uma mensagem de sucesso é retornada. Caso contrário, uma mensagem de erro é retornada, indicando que o registro não pode ser excluído porque já foi finalizado.
Lembre-se de incluir na documentação do README informações adicionais, como a estrutura esperada do objeto JSON para o endpoint de registro de veículo (RegistroVeiculo) e exemplos de uso para cada API.
