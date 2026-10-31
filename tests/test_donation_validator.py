import os
import pytest
from src.validators.donation_validator import DonationValidator


class TestDonationValidator:
    """Testes unitários para o validador de itens de doação."""

    @pytest.mark.parametrize("item_valido", [
        {
            "titulo": "Kit de Geometria e Compasso",
            "categoria": "Material Escolar",
            "estado_conservacao": "Novo",
        },
        {
            "titulo": "Mochila Infantil",
            "categoria": "Acessórios",
            "estado_conservacao": "Bom estado",
        },
        {
            "titulo": "Caderno Universitário 10 Matérias",
            "categoria": "Papelaria",
            "estado_conservacao": "Novo",
        },
    ])
    def test_cadastro_doacao_valida(self, item_valido):
        """Deve validar com sucesso itens que possuem todos os campos obrigatórios."""
        validador = DonationValidator(item_valido)
        assert validador.valida_doacao() is True

    @pytest.mark.parametrize("item_incompleto", [
        {
            "titulo": "",
            "categoria": "Livros Didáticos",
            "estado_conservacao": "Bom estado",
        },
        {
            "titulo": "   ",
            "categoria": "Papelaria",
            "estado_conservacao": "Novo",
        },
        {
            "titulo": "Estojo Escolar",
            "categoria": "",
            "estado_conservacao": "Usado",
        },
        {
            "titulo": "Lápis de Cor",
            "categoria": "Material Escolar",
            "estado_conservacao": "   ",
        },
    ])
    def test_rejeita_doacao_com_campo_vazio(self, item_incompleto):
        """Itens com campos obrigatórios vazios ou apenas com espaços devem ser recusados."""
        validador = DonationValidator(item_incompleto)
        assert validador.valida_doacao() is False

    @pytest.mark.parametrize("item_sem_chave", [
        {
            "titulo": "Mochila Infantil",
            "categoria": "Acessórios",
        },
        {
            "titulo": "Livro de Matemática",
            "estado_conservacao": "Bom estado",
        },
        {
            "categoria": "Papelaria",
            "estado_conservacao": "Novo",
        },
        {},
    ])
    def test_rejeita_doacao_sem_campos_obrigatorios(self, item_sem_chave):
        """A ausência de qualquer chave obrigatória no dicionário deve reprovar o cadastro."""
        validador = DonationValidator(item_sem_chave)
        assert validador.valida_doacao() is False

    def test_estrutura_diretorio_src_existe(self):
        """Garante que os diretórios principais de código-fonte existem para o build."""
        assert os.path.isdir("src") is True
        assert os.path.isdir("src/validators") is True