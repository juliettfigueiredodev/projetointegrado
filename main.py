from src.models.entities import Donor, Institution
from src.infrastructure.user_db import UserDB

def main():
    db = UserDB()

    print("=== Cadastro EducaSolidário ===")
    
    try:
        # Coleta de dados (Simulando o Frontend)
        print("Preencha os dados do Doador:")
        # O input fica AQUI, não dentro da classe
        email_input = input("Email: ") 
        pass_input = input("Senha: ")
        
        # Instanciação (Isso aciona as validações dos Setters nos Models)
        # Se o email for inválido, o erro estoura aqui e é pego pelo 'except'
        novo_doador = Donor(
            user_id=1,
            email=email_input,
            password=pass_input,
            endereco="Rua dos Bugs, 123",
            telefone="1199999999",
            cpf="123.456.789-00",
            name="João Silva",
            date_birth="1990-01-01"
        )
        
        # Persistência
        db.save(novo_doador)

    except ValueError as e:
        print(f"Erro de Validação: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()