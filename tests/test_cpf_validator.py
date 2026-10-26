import pytest
from src.validators.cpf_validator import CPFValidator


class TestCPFValidator:
    """Testes unitários para o validador de CPF."""

    @pytest.mark.parametrize("cpf_valido", [
        "52998224725",
        "529.982.247-25",
        "00000000191",
        "000.000.001-91",
    ])
    def test_cpf_valido(self, cpf_valido):
        """Deve validar com sucesso CPFs matematicamente válidos, com ou sem formatação."""
        validador = CPFValidator(cpf_valido)
        assert validador.valida_cpf() is True

    @pytest.mark.parametrize("cpf_digitos_iguais", [
        "00000000000",
        "11111111111",
        "222.222.222-22",
        "999.999.999-99",
    ])
    def test_cpf_com_digitos_iguais_invalido(self, cpf_digitos_iguais):
        """CPFs com todos os dígitos repetidos devem ser considerados inválidos."""
        validador = CPFValidator(cpf_digitos_iguais)
        assert validador.valida_cpf() is False

    @pytest.mark.parametrize("cpf_tamanho_invalido", [
        "",
        "123",
        "1234567890",
        "123456789012",
        "123.456.78-9",
    ])
    def test_cpf_tamanho_invalido(self, cpf_tamanho_invalido):
        """CPFs que não possuem exatamente 11 dígitos numéricos devem ser recusados."""
        validador = CPFValidator(cpf_tamanho_invalido)
        assert validador.valida_cpf() is False

    @pytest.mark.parametrize("cpf_digito_incorreto", [
        "52998224720",
        "529.982.247-24",
        "000.000.001-90",
    ])
    def test_cpf_digito_verificador_incorreto(self, cpf_digito_incorreto):
        """CPFs com dígitos verificadores inconsistentes com a fórmula devem ser recusados."""
        validador = CPFValidator(cpf_digito_incorreto)
        assert validador.valida_cpf() is False
