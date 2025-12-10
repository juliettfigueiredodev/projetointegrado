import User

class Donor(User):
   def __init__(self, cpf, donor_name, date_birth, user_id, user_type, email, password, endereco, telefone):
      super().__init__(user_id, user_type, email, password, endereco, telefone)
      self.cpf = cpf #precisa validar
      self.donor_name = donor_name
      self.date_birth = date_birth