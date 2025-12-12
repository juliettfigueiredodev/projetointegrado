import re #Importa a  biblioteca de expressões regulares

class PhoneValidator: #Define a classe para validar e formatar telefones brasileiros

    PADRAO = re.compile(r"^(\d{2})(9\d{8}|[2-5]\d{7})$") #Define o padrão regex para telefones brasileiros

    def __init__(self, telefone):
        if self.valida_telefone(telefone): #Verifica se o telefone é valido.
            self.numero = telefone #se for válido, armazena no objeto.
        else:
            raise ValueError("Número invalido") #caso contrario, da erro.

    def __str__(self): #Define como o objeto deve ser convertido em string.
        return self.format_numero() #Retorna o número formatado.

    def valida_telefone(self, telefone): 
        return bool(self.PADRAO.fullmatch(telefone)) #Retorna True se o telefone corresponder exatamente ao padrão regex que foi definido.

    def format_numero(self): #Método para formatar o número validado
        match = self.PADRAO.fullmatch(self.numero) #Faz o match do número com o padrão regex.
        ddd, resto = match.group(1), match.group(2) #Extrai o DDD e o resto do número.

        if len(resto) == 9:  #Se tiver 9 dígitos, é celular
            return f"({ddd}) {resto[:5]}-{resto[5:]}"
            #Formata como: (XX) 99999-9999
        else:                #Se não tiver 9 dígitos, é fixo (8 dígitos)
            return f"({ddd}) {resto[:4]}-{resto[4:]}"
            #Formata como: (XX) 1234-5678
