from .User import User #Classe mãe
from src.services import Email #validação
from src.services import Cpf #validação
from src.services import Phone #validação

class Donor(User): #Herança - classe filha de User
   #inicializa a classe Donor
   def __init__(self, cpf, donor_name, date_birth, user_id, user_type, email, password, endereco, telefone): 
      # herda atributos da classe mãe
      super().__init__(user_id, user_type, email, password, endereco, telefone) 
      #chama método de validação de Email
      Email.valida_email(email) 

      #chama método de validação de Cpf
      Cpf.valida_cpf(cpf)
      #chama método de validação de Telefone
      Phone.valida_telefone(telefone)

      self.donor_name = donor_name
      self.date_birth = date_birth

      

