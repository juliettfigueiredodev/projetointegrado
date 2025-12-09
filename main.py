from src.models import Donor, Institution
from src.infrastructure import UserDB

def main():
    db = UserDB()

    print("=== Cadastro EducaSolidário ===")
    print("1 - Quero ser um Doador")
    print("2 - Sou uma Instituição")
    opcao = input("Escolha sua opção: ")
    
    try:
        # Dados comuns a ambos (Email, Senha, Endereço, Telefone)
        print("\n--- Dados de Acesso ---")
        email_input = input("Email: ") 
        pass_input = input("Senha: ")
        addr_input = input("Endereço: ")
        phone_input = input("Telefone: ")

        novo_usuario = None # Variável que vai guardar o objeto criado
        
        if opcao == '1':
            print("\n--- Dados do Doador ---")
            cpf_input = input("CPF: ")
            name_input = input("Nome Completo: ")
            birth_input = input("Data de Nascimento: ")

            novo_usuario = Donor(
                user_id=1, # Num sistema real, isso seria gerado automaticamente
                email=email_input,
                password=pass_input,
                endereco=addr_input,
                telefone=phone_input,
                cpf=cpf_input,
                name=name_input,
                date_birth=birth_input
            )

        elif opcao == '2':
            print("\n--- Dados da Instituição ---")
            cnpj_input = input("CNPJ: ")
            inst_name_input = input("Nome da Instituição: ")

            novo_usuario = Institution(
                user_id=2,
                email=email_input,
                password=pass_input,
                endereco=addr_input,
                telefone=phone_input,
                cnpj=cnpj_input,
                institution_name=inst_name_input
            )
        else:
            print("Opção inválida! Reinicie o programa.")
            return
        
        # Persistência
        # O método .save() funciona para ambos graças ao Polimorfismo
        if novo_usuario:
            db.save(novo_usuario)

    except ValueError as e:
        print(f"\n[ERRO DE VALIDAÇÃO]: {e}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")

if __name__ == "__main__":
    main()