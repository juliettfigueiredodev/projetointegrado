import pytest
from src.validators.email_validator import EmailValidator


class TestEmailValidator:
    """Testes unitários para o validador de e-mail."""

    @pytest.mark.parametrize("email_valido", [
        "usuario@dominio.com",
        "doador.solidario@ong.org.br",
        "contato+projeto@escola.edu.br",
        "aluno123@ufca.edu.br",
    ])
    def test_email_valido(self, email_valido):
        """Deve instanciar com sucesso para e-mails em formato padrão válido."""
        validador = EmailValidator(email_valido)
        assert str(validador) == email_valido
        assert validador.valida_email(email_valido) is True

    @pytest.mark.parametrize("email_invalido", [
        "",
        "usuario@",
        "@dominio.com",
        "usuario@dominio",
        "usuario @dominio.com",
        "usuario@dominio.c",
        "usuario sem arroba",
    ])
    def test_email_invalido_lanca_excecao(self, email_invalido):
        """Deve lançar ValueError para formatos de e-mail incompatíveis com a regra."""
        with pytest.raises(ValueError, match="Email inválido"):
            EmailValidator(email_invalido)
