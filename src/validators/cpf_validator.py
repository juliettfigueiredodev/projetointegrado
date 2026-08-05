import re

class CPFValidator:
    def __init__(self, cpf):

        self.cpf = cpf
        
    def _limpar_cpf(self):
        #Remove pontos e hífens do CPF
        return re.sub(r'[^0-9]', '', self.cpf)

    def _validar_formato(self, cpf_limpo):
        #Verifica se o CPF tem 11 dígitos e não é uma sequência repetida
        if len(cpf_limpo) != 11:
            return False
        # Verifica CPFs com todos os dígitos iguais, que são inválidos
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        return True

    def _calcular_digito(self, cpf_parcial, peso_inicial):
        #Calcula um dígito verificador com base no algoritmo do CPF
        soma = 0
        for i, digito in enumerate(cpf_parcial):
            soma += int(digito) * (peso_inicial - i) 
        
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto 

    def valida_cpf(self):
        #Realiza a validação completa do CPF
        cpf_limpo = self._limpar_cpf()

        if not self._validar_formato(cpf_limpo):
            return False

        # Validação do primeiro dígito verificador
        nove_digitos = cpf_limpo[:9]
        primeiro_digito_calc = self._calcular_digito(nove_digitos, 10)
        
        # Validação do segundo dígito verificador
        dez_digitos = nove_digitos + str(primeiro_digito_calc)
        segundo_digito_calc = self._calcular_digito(dez_digitos, 11)

        # Verifica se os dígitos calculados coincidem com os dígitos reais
        return (int(cpf_limpo[9]) == primeiro_digito_calc) and \
               (int(cpf_limpo[10]) == segundo_digito_calc)

