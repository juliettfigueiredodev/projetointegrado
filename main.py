from classes_ import *

user = User(
    user_id=1,
    user_type='donor',
    email='teste@gmail.com',
    password='senha1234',
    endereco='Rua A, 123',
    telefone='8899999999'
)

dados = user.send_to_bd()
print(dados)
