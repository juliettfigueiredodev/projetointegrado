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
        proibidos = "[]{}()=+\çÇ´`^~ ;'/"
        
        #Conta se a senha tem no minimo 8 digitos
        if len(new_password) < 8: 
            raise ValueError('Senha muito curta.')
        
        #loop para verificar se a senha tem caracteres proibidos, da para melhorar é só um rascunho
        for caractere in new_password: 
           if caractere in proibidos:
              raise ValueError('Senha contém caracteres proibidos')
           
        self.__password = new_password
           

    def send_to_bd(self):
        return {
        'user_id': self.user_id,
        'user_type': self.user_type,
        'email': self.email,
        'password': self.password,
        'endereco': self.endereco,
        'telefone': self.telefone
        }





