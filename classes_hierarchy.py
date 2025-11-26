class User: #superclass
    def __init__(self, user_id, user_type, email, password, endereco, telefone):
        self.user_id = user_id
        self.user_type = user_type
        self.endereco = endereco
        self.telefone = telefone
        self.__email = email
        self.__password = password

    # Getters e Setters - métodos para acesso aos atributos name-mangling #
    @property
    def email(self): #getter
        return self.__email
    
    @email.setter 
    def email(self, new_email):
        new_email = input('Digite o email: ')
        if isinstance(new_email, str):
           if ('@' in new_email and '.' in new_email):
            self.__email = new_email
            return f'Email {self.__email} cadastrado com sucesso!'
           else:
              raise ValueError('Email inválido. Tente novamente')
        else:
           raise ValueError('Email inválido, tente novamente!')
        
    @property
    def password(self):
       return self.__password
    
    @password.setter
    def password(self, new_password):
       pass

    def send_to_bd(self):
       pass

class Donor(User):
   def __init__(self, user_id, user_type, email, password, endereco, telefone):
      super().__init__(user_id, user_type, email, password, endereco, telefone)
      self.number_id = cpf
      self.name = name_donor
      self.date_birth = date_birth


class Institution(User):
   def __init__(self, user_id, user_type, email, password, endereco, telefone):
      super().__init__(user_id, user_type, email, password, endereco, telefone)
      self.institution_reg_number = cnpj
      self.institution_name = institution_name

