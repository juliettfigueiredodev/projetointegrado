from .user import User #Classe mãe
from src.validators import EmailValidator #validação
from src.validators import CPFValidator #validação
from src.validators import PhoneValidator #validação

class Donor(User): #Herança - classe filha de User
   #inicializa a classe Donor
   def __init__(self, cpf, name, date_birth, user_id, user_type, email, password, endereco, telefone): 
      # herda atributos da classe mãe
      super().__init__(user_id, user_type, email, password, endereco, telefone) 
      #chama método de validação de Email
      EmailValidator.valida_email(email) 

      #chama método de validação de Cpf
      CPFValidator.valida_cpf(cpf)
      #chama método de validação de Telefone
      PhoneValidator.valida_telefone(telefone)

      self.name = name
      self.date_birth = date_birth

      

