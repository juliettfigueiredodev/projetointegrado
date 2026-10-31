import re

class Registro:
    # Regex que aceita CPF ou CNPJ com ou sem pontuação
    REGEX = re.compile(
        r'^(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})$'
    )

    def __init__(self, valor: str):
        self.raw = valor                                # Texto original informado
        self.numeros = re.sub(r'\D', '', valor or '')   # Remove tudo que não for dígito

    def formato_valido(self) -> bool:
        return bool(self.REGEX.fullmatch(self.raw))     # Verifica se o formato é de CPF ou CNPJ

    def tipo(self) -> str:
        # Determina pelo total de dígitos
        return "CPF" if len(self.numeros) == 11 else \
               "CNPJ" if len(self.numeros) == 14 else \
               "Inválido"

    def is_valid(self) -> bool:
        # Aceita apenas se o formato é válido e tem quantidade correta de dígitos
        return self.formato_valido() and self.tipo() in ("CPF", "CNPJ")

    def formatado(self) -> str:
        n = self.numeros
        # Formata conforme tipo detectado
        if self.tipo() == "CPF":
            return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"
        if self.tipo() == "CNPJ":
            return f"{n[:2]}.{n[2:5]}.{n[5:8]}/{n[8:12]}-{n[12:]}"
        return n  # Se inválido, devolve só os dígitos

    def __str__(self) -> str:
        return self.formatado()     # Exibe formatado ao usar print()



