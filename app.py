import os
from flask import Flask, request
from Controllers import routeController
rc = routeController.RouteControl()
from Controllers import inputController
ic = inputController.InputControl()
from Controllers import authController
ac = authController.AuthControl()


os.system("python -m pytest")

app = Flask(__name__)


@app.route("/user/auth/register", methods=['POST'])
def register_route():
    """Rota de registro de usuário
    Verificar o json recebido e chamar o controller da rota.

    Returns:
        tuple(content, statuscode): Retorna o id do usuário registrado e o statuscode, em caso de erro retorna a mensagem de erro.
    """
    if not ac.access_key_validation(dict(request.headers)):
        return "Invalid access key.", 401
    
    transfrom_to_dict = ic.json_to_dict(request)
    if transfrom_to_dict[1] != 200:
        return transfrom_to_dict
    result = rc.register_route(transfrom_to_dict[0])
    return result

@app.route("/user/auth/login", methods=['POST'])
def login_route():
    """Rota de login de usuário
    Verificar o json recebido e chamar o controller da rota de login.
    
    Returns:
        tuple(content, statuscode): Retorna o id do usuário conectado e o statuscode, em caso de erro retorna a mensagem de erro.
    """	
    if not ac.access_key_validation(dict(request.headers)):
        return "Invalid access key.", 401

    transfrom_to_dict = ic.json_to_dict(request)
    if transfrom_to_dict[1] != 200:
        return transfrom_to_dict
    result = rc.login_route(transfrom_to_dict[0])
    return result

@app.route("/user/auth/token/<string:value>", methods=['POST', 'GET'])
def validate_recover_route(value):
    """Rota de geração/validação de token
    Chamar o controller da rota de gerar/validar token.

    Args:
        value (str): Email a receber o token / Token a ser validado.

    Returns:
        tuple(content, statuscode): Retorna o ID do usuário e o statuscode, em caso de erro retorna a mensagem e o statuscode.
    """
    if request.method == "POST":
        return rc.recover_route(value)
    elif request.method == "GET":
        return rc.validate_recover_route(value)
        
@app.route("/user/address", methods=['POST', 'PUT'])
def address_route():
    """Rota de Cadastro/Atualização de Endereço
    Verificar o json recebido e chamar o controller da rota de endereço.

    Returns:
        tuple(content, statuscode): Retorna o id do usuário conectado e o statuscode, em caso de erro retorna a mensagem de erro.
    """
    transfrom_to_dict = ic.json_to_dict(request)
    if transfrom_to_dict[1] != 200:
        return transfrom_to_dict
    result = rc.set_address_route(transfrom_to_dict[0])
    return result

#Essa rota precisa estar segura, apenas pode ser acessada com a permissão do front.
@app.route("/user/account/password", methods=['POST'])
def change_password_route():
    transfrom_to_dict = ic.json_to_dict(request)
    if transfrom_to_dict[1] != 200:
        return transfrom_to_dict
    result = rc.change_password_route(transfrom_to_dict[0])
    return result

@app.route("/user/<string:id>")
def get_user_by_id_route(id):
    if not ac.access_key_validation(dict(request.headers)):
        return "Invalid access key.", 401
        
    result = rc.get_user_by_id_route(id)
    return result

@app.route("/users/list", methods=['GET', 'POST'])
def get_users_by_id_route():
    """
    Rota para listar todos os usuário que foram requisitados por uma lista dentro de um campo json chamado "_id"

    Returns:
        Uma lista de dicionários passando todos os usuários que foram pedidos.
    """
    get_request = request.get_json()
    return rc.get_users_by_id_route(get_request)  
 
if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5030)