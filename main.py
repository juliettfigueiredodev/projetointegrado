from src.models.User import *

#AREA DE TESTES, FAVOR IGNORAR
user1 = User('1', 'donor', 'teste@gmail.com', 12345678, 'rua teste, 512, Crato', 8888888888)

dados = user1.send_to_bd()
print(dados)

user1.password = "123()8899"