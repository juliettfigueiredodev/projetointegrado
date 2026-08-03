import re #módulo de expressões regulares

#classe para validar email para as classes Donor e Institution
class EmailValidator: 
    # antes e depois do @ recebe letras e alguns caracteres especiais, espera-se . e depois apenas letras limitando a quantidade (2 a 3)
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})*$'

    #inicializa o objeto da classe
    def __init__(self, email):
        #apenas guarda o valor se o método de validação retornar True e retorna mensagem
        if self.valida_email(email): 
            self.email = email        
        #retorna mensagem de erro, caso o método retorne False
        else: raise ValueError ('Email inválido')

    #retorno padrão do email digitado
    def __str__(self):
        return self.email

    def valida_email(self, email):
         
        #compara o regex com a entrada e caso email seguir a expressão retorna verdadeiro, caso contrário, retorna falso
        return bool(re.fullmatch(self.regex, email))
        
