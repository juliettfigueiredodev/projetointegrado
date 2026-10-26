import pytest
from src.validators.phone_validator import PhoneValidator


class TestPhoneValidator:
    """Testes unitários para o validador e formatador de telefone."""

    def test_celular_valido_com_formatacao(self):
        """Deve aceitar celular brasileiro (DDD + 9 dígitos começando com 9) e formatar corretamente."""
        validador = PhoneValidator("88998765432")
        assert validador.format_numero() == "(88) 99876-5432"
        assert str(validador) == "(88) 99876-5432"

    def test_telefone_fixo_valido_com_formatacao(self):
        """Deve aceitar telefone fixo brasileiro (DDD + 8 dígitos iniciando entre 2 e 5) e formatar."""
        validador = PhoneValidator("8835123456")
        assert validador.format_numero() == "(88) 3512-3456"
        assert str(validador) == "(88) 3512-3456"

    @pytest.mark.parametrize("telefone_invalido", [
        "",
        "1234567",
        "88898765432",   # celular sem o 9 inicial no corpo (ex: começa com 8)
        "8812345678",    # fixo iniciando com 1 (fora de 2-5)
        "8899876543210",  # dígitos em excesso
        "telefone_abc",
    ])
    def test_telefone_invalido_lanca_excecao(self, telefone_invalido):
        """Deve lançar ValueError para telefones em padrão fora da convenção nacional."""
        with pytest.raises(ValueError, match="Número invalido"):
            PhoneValidator(telefone_invalido)
