class UserDB:
    def __init__(self):
        # Simulando um banco de dados em memória
        self.database = []

    def save(self, user):
        """
        Recebe um objeto do tipo User (ou filhos) e salva.
        Isso substitui o 'send_to_bd' de dentro da classe.
        """
        try:
            # Aqui entraria o código SQL ou ORM (SQLAlchemy, Django, etc)
            print(f"--- Conectando ao BD... ---")
            
            data = {
                "id": user.user_id,
                "type": user.user_type,
                "email": user.email,
                "endereco": user.endereco
            }
            
            # Adiciona campos específicos dependendo do tipo
            if user.user_type == 'donor': # Doador
                data['name'] = user.name
                data['cpf'] = user.cpf
                print(f"Salvando Doador: {user.name}")
                
            elif user.user_type == 'institution': # Instituição
                data['institution_name'] = user.institution_name
                data['cnpj'] = user.cnpj
                print(f"Salvando Instituição: {user.institution_name}")

            self.database.append(data)
            print("Dados persistidos com sucesso!\n")
            return True
        
        except AttributeError as e:
            # Esse erro vai acontecer se o tipo for 'donor' mas o objeto não tiver 'name'
            print(f"Erro de Integridade: O tipo é {user.user_type}, mas faltou atributo: {e}")
            return False
        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")
            return False