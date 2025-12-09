import re

class TelefonesBr:

    PADRAO = re.compile(r"^(\d{2})(9\d{8}|[2-5]\d{7})$")

    def __init__(self, telefone):
        if self.valida_telefone(telefone):
            self.numero = telefone
        else:
            raise ValueError("Número invalido")

    def __str__(self):
        return self.format_numero()

    def valida_telefone(self, telefone):
        return bool(self.PADRAO.fullmatch(telefone))

    def format_numero(self):
        match = self.PADRAO.fullmatch(self.numero)
        ddd, resto = match.group(1), match.group(2)

        if len(resto) == 9:  # Celular
            return f"({ddd}) {resto[:5]}-{resto[5:]}"
        else:                # Fixo
            return f"({ddd}) {resto[:4]}-{resto[4:]}"
