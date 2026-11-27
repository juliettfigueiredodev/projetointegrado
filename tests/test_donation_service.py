import pytest
from src.services.donation_service import DonationService
from src.models.donation import Donation
from src.models.user import User


class TestDonationService:
    """Testes unitários para a regra de negócio do serviço de doações."""

    @pytest.fixture
    def service(self):
        return DonationService()

    @pytest.fixture
    def item_valido(self):
        return {
            "titulo": "Caderno Universitário 10 Matérias",
            "categoria": "Papelaria",
            "estado_conservacao": "Novo",
        }

    @pytest.fixture
    def donor_mock(self):
        return User(
            user_id=10,
            user_type="donor",
            email="doador@exemplo.com",
            password="SenhaForte123",
            endereco="Rua das Flores, 123",
            telefone="11999998888",
        )

    @pytest.fixture
    def institution_mock(self):
        return User(
            user_id=20,
            user_type="institution",
            email="escola@exemplo.com",
            password="SenhaForte123",
            endereco="Av. Principal, 456",
            telefone="11988887777",
        )

    def test_registrar_doacao_com_sucesso(self, service, donor_mock, institution_mock, item_valido):
        """Deve registrar uma doação com status inicial 'pendente'."""
        doacao = service.registrar_doacao(
            donor=donor_mock,
            institution=institution_mock,
            item_data=item_valido,
            quantity=3,
            notes="Entrega prevista para sábado",
        )

        assert doacao.donation_id == 1
        assert doacao.donor_id == 10
        assert doacao.institution_id == 20
        assert doacao.quantity == 3
        assert doacao.status == Donation.STATUS_PENDENTE
        assert doacao.notes == "Entrega prevista para sábado"

    def test_registrar_doacao_com_ids_inteiros(self, service, item_valido):
        """Deve permitir registrar doação passando diretamente IDs numéricos válidos."""
        doacao = service.registrar_doacao(
            donor=1,
            institution=2,
            item_data=item_valido,
            quantity=1,
        )
        assert doacao.donor_id == 1
        assert doacao.institution_id == 2
        assert doacao.status == Donation.STATUS_PENDENTE

    def test_rejeitar_doacao_para_si_mesmo(self, service, item_valido):
        """Usuário não pode doar para si mesmo."""
        with pytest.raises(ValueError, match="mesmo usuário"):
            service.registrar_doacao(
                donor=5,
                institution=5,
                item_data=item_valido,
                quantity=1,
            )

    def test_rejeitar_item_invalido(self, service, donor_mock, institution_mock):
        """Deve rejeitar quando o item de doação não atende às regras do DonationValidator."""
        item_incompleto = {
            "titulo": "",
            "categoria": "Papelaria",
            "estado_conservacao": "Novo",
        }
        with pytest.raises(ValueError, match="Dados do item inválidos"):
            service.registrar_doacao(
                donor=donor_mock,
                institution=institution_mock,
                item_data=item_incompleto,
            )

    @pytest.mark.parametrize("quantidade_invalida", [0, -1, -5, "duas", None])
    def test_rejeitar_quantidade_invalida(self, service, donor_mock, institution_mock, item_valido, quantidade_invalida):
        """Deve rejeitar quantidade zero, negativa ou não numérica."""
        with pytest.raises(ValueError, match="maior que zero"):
            service.registrar_doacao(
                donor=donor_mock,
                institution=institution_mock,
                item_data=item_valido,
                quantity=quantidade_invalida,  # type: ignore
            )

    def test_rejeitar_perfil_incorreto(self, service, item_valido):
        """Usuário do tipo institution não pode doar como donor."""
        usuario_invalido = User(
            user_id=1,
            user_type="institution",
            email="inst@exemplo.com",
            password="SenhaForte123",
            endereco="Rua A",
            telefone="11999999999",
        )
        with pytest.raises(ValueError, match="perfil de doador"):
            service.registrar_doacao(
                donor=usuario_invalido,
                institution=2,
                item_data=item_valido,
            )

    def test_ciclo_de_vida_completo_da_doacao(self, service, donor_mock, institution_mock, item_valido):
        """Testa o fluxo feliz completo: pendente -> confirmada -> entregue."""
        doacao = service.registrar_doacao(
            donor=donor_mock,
            institution=institution_mock,
            item_data=item_valido,
            quantity=2,
        )
        assert doacao.status == Donation.STATUS_PENDENTE

        # Confirma doação
        doacao_confirmada = service.confirmar_doacao(doacao.donation_id)
        assert doacao_confirmada.status == Donation.STATUS_CONFIRMADA

        # Marca como entregue
        doacao_entregue = service.marcar_como_entregue(doacao.donation_id)
        assert doacao_entregue.status == Donation.STATUS_ENTREGUE

    def test_transicoes_invalidas_de_status(self, service, donor_mock, institution_mock, item_valido):
        """Não pode entregar doação sem antes confirmar."""
        doacao = service.registrar_doacao(
            donor=donor_mock,
            institution=institution_mock,
            item_data=item_valido,
        )
        with pytest.raises(ValueError, match="Apenas doações com status 'confirmada'"):
            service.marcar_como_entregue(doacao.donation_id)

    def test_cancelamento_de_doacao_pendente(self, service, donor_mock, institution_mock, item_valido):
        """Doação pendente pode ser cancelada informando motivo."""
        doacao = service.registrar_doacao(
            donor=donor_mock,
            institution=institution_mock,
            item_data=item_valido,
        )
        cancelada = service.cancelar_doacao(doacao.donation_id, motivo="Sem disponibilidade de entrega")
        assert cancelada.status == Donation.STATUS_CANCELADA
        assert "Cancelamento: Sem disponibilidade de entrega" in (cancelada.notes or "")

    def test_nao_pode_cancelar_doacao_entregue(self, service, donor_mock, institution_mock, item_valido):
        """Doação que já foi entregue não pode ser cancelada."""
        doacao = service.registrar_doacao(
            donor=donor_mock,
            institution=institution_mock,
            item_data=item_valido,
        )
        service.confirmar_doacao(doacao.donation_id)
        service.marcar_como_entregue(doacao.donation_id)

        with pytest.raises(ValueError, match="já entregues não podem ser canceladas"):
            service.cancelar_doacao(doacao.donation_id)

    def test_listar_por_doador_e_instituicao(self, service, item_valido):
        """Testa listagem e filtros por doador e instituição."""
        service.registrar_doacao(donor=100, institution=200, item_data=item_valido, quantity=1)
        d2 = service.registrar_doacao(donor=100, institution=201, item_data=item_valido, quantity=2)
        service.registrar_doacao(donor=101, institution=200, item_data=item_valido, quantity=3)

        service.confirmar_doacao(d2.donation_id)

        # Filtro por doador
        doacoes_100 = service.listar_por_doador(100)
        assert len(doacoes_100) == 2

        doacoes_100_confirmadas = service.listar_por_doador(100, status=Donation.STATUS_CONFIRMADA)
        assert len(doacoes_100_confirmadas) == 1
        assert doacoes_100_confirmadas[0].donation_id == d2.donation_id

        # Filtro por instituição
        doacoes_inst_200 = service.listar_por_instituicao(200)
        assert len(doacoes_inst_200) == 2
