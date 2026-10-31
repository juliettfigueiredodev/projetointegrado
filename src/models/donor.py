from .user import User #Classe mãe
from src.validators import EmailValidator #validação
from src.validators import CPFValidator #validação
from src.validators import PhoneValidator #validação
from datetime import datetime

class Donor(User): #Herança - classe filha de User
   #inicializa a classe Donor
   def __init__(self, cpf, name, date_birth, user_id, user_type, email, password, endereco, telefone): 
      try:
          converted_data = datetime.strptime(date_birth, "%d/%m/%Y").strftime("%Y-%m-%d")
      except ValueError:
          raise ValueError("Formato de data inválido. Use dia/mês/ano (ex: 21/06/1996)")
      
      # herda atributos da classe mãe
      super().__init__(user_id, user_type, email, password, endereco, telefone) 
      #chama método de validação de Email
      EmailValidator(email) 

      #chama método de validação de Cpf
      CPFValidator(cpf).valida_cpf()
      #chama método de validação de Telefone
      PhoneValidator(telefone)

      self.name = name
      self.cpf = cpf
      self.date_birth = converted_data
