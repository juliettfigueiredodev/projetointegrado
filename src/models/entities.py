class User:
    def __init__(self, user_id, user_type, email, password, endereco, telefone):
        self.user_id = user_id
        self.user_type = user_type
        self.endereco = endereco
        self.telefone = telefone
        # Atributos protegidos (encapsulamento)
        self._email = None 
        self._password = None
        
        # Usamos os setters para validar na inicialização
        self.email = email
        self.password = password

    @property
    def email(self):
        return self._email
    
    @email.setter 
    def email(self, new_email):
        # Validação pura: sem input, apenas verifica e aceita ou erra.
        if isinstance(new_email, str) and '@' in new_email and '.' in new_email:
            self._email = new_email
        else:
            raise ValueError(f"Email '{new_email}' é inválido.")

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, new_password):
        # Validação de senha (exemplo: mínimo 6 caracteres)
        if isinstance(new_password, str) and len(new_password) >= 6:
            self._password = new_password
        else:
            raise ValueError("A senha deve ter no mínimo 6 caracteres.")

class Donor(User):
    def __init__(self, user_id, email, password, endereco, telefone, cpf, name, date_birth):
        # Chama o construtor do pai, definindo user_type fixo
        super().__init__(user_id, 'donor', email, password, endereco, telefone)
        self.cpf = cpf
        self.name = name
        self.date_birth = date_birth

class Institution(User):
    def __init__(self, user_id, email, password, endereco, telefone, cnpj, institution_name):
        super().__init__(user_id, 'institution', email, password, endereco, telefone)
        self.cnpj = cnpj
        self.institution_name = institution_name