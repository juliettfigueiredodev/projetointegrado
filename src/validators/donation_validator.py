class DonationValidator:
    """Validador para os dados de cadastro de itens de doação."""

    def __init__(self, dados_item):
        self.dados_item = dados_item
        self.campos_obrigatorios = ["titulo", "categoria", "estado_conservacao"]

    def valida_doacao(self):
        if not isinstance(self.dados_item, dict):
            return False

        for campo in self.campos_obrigatorios:
            valor = self.dados_item.get(campo)
            if not valor or not str(valor).strip():
                return False

        return True