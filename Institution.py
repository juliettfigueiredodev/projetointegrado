import User

class Institution(User):
   def __init__(self, cnpj, institution_name, user_id, user_type, email, password, endereco, telefone):
      super().__init__(user_id, user_type, email, password, endereco, telefone)
      self.cnpj = cnpj
      self.institution_name = institution_name
