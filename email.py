import re

class email:
    
    def __init__(self, email):
        self.email = email

    def valida_email(self, email):
        regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z][2-7]'
        return 'Email Válido' if re.fullmatch(regex,email) else 'Email inválido'