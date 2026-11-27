from typing import List, Optional, Dict, Any, Union
from src.models.user import User
from src.models.donor import Donor
from src.models.institution import Institution
from src.models.donation import Donation
from src.validators.donation_validator import DonationValidator


class DonationService:
    """Serviço de domínio responsável pela lógica de negócios de doações."""

    def __init__(self, repository: Optional[Any] = None) -> None:
        """
        repository: Opcional. Permite desacoplar a persistência (in-memory ou DB).
        Se nenhum repositório for fornecido, utiliza armazenamento em memória.
        """
        self._repository = repository
        self._donations: Dict[int, Donation] = {}
        self._next_id: int = 1

    def registrar_doacao(
        self,
        donor: Union[Donor, User, int],
        institution: Union[Institution, User, int],
        item_data: Dict[str, Any],
        quantity: int = 1,
        notes: Optional[str] = None,
    ) -> Donation:
        """
        Registra uma nova intenção de doação de materiais escolares.
        Valida perfis, integridade do item e quantidade mínima.
        """
        donor_id = self._extrair_e_validar_donor(donor)
        institution_id = self._extrair_e_validar_institution(institution)

        if donor_id == institution_id:
            raise ValueError("O doador e a instituição não podem ser o mesmo usuário.")

        validador = DonationValidator(item_data)
        if not validador.valida_doacao():
            raise ValueError(
                "Dados do item inválidos. Verifique se 'titulo', 'categoria' e "
                "'estado_conservacao' estão preenchidos."
            )

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("A quantidade doada deve ser um número inteiro maior que zero.")

        donation_id = self._next_id
        self._next_id += 1

        donation = Donation(
            donation_id=donation_id,
            donor_id=donor_id,
            institution_id=institution_id,
            item=item_data,
            quantity=quantity,
            status=Donation.STATUS_PENDENTE,
            notes=notes,
        )

        self._donations[donation_id] = donation
        if self._repository and hasattr(self._repository, "save_donation"):
            self._repository.save_donation(donation)

        return donation

    def realizar_doacao(
        self,
        donor: Union[Donor, User, int],
        institution: Union[Institution, User, int],
        item_data: Dict[str, Any],
        quantity: int = 1,
        notes: Optional[str] = None,
    ) -> Donation:
        """Alias mantido para consistência semântica com o protótipo inicial."""
        return self.registrar_doacao(
            donor=donor,
            institution=institution,
            item_data=item_data,
            quantity=quantity,
            notes=notes,
        )

    def confirmar_doacao(self, donation_id: int) -> Donation:
        """Instituição confirma o interesse/recebimento preliminar da doação."""
        donation = self.obter_doacao(donation_id)
        if donation.status != Donation.STATUS_PENDENTE:
            raise ValueError(
                f"Apenas doações com status '{Donation.STATUS_PENDENTE}' podem ser confirmadas. "
                f"Status atual: '{donation.status}'."
            )
        donation.status = Donation.STATUS_CONFIRMADA
        return donation

    def marcar_como_entregue(self, donation_id: int) -> Donation:
        """Finaliza a doação quando o material escolar é entregue com sucesso."""
        donation = self.obter_doacao(donation_id)
        if donation.status != Donation.STATUS_CONFIRMADA:
            raise ValueError(
                f"Apenas doações com status '{Donation.STATUS_CONFIRMADA}' podem ser marcadas como entregues. "
                f"Status atual: '{donation.status}'."
            )
        donation.status = Donation.STATUS_ENTREGUE
        return donation

    def cancelar_doacao(self, donation_id: int, motivo: Optional[str] = None) -> Donation:
        """Cancela uma doação em andamento (pendente ou confirmada)."""
        donation = self.obter_doacao(donation_id)
        if donation.status == Donation.STATUS_ENTREGUE:
            raise ValueError("Doações já entregues não podem ser canceladas.")
        if donation.status == Donation.STATUS_CANCELADA:
            raise ValueError("Esta doação já está cancelada.")

        donation.status = Donation.STATUS_CANCELADA
        if motivo:
            prefixo = f"{donation.notes} - " if donation.notes else ""
            donation.notes = f"{prefixo}[Cancelamento: {motivo}]"
        return donation

    def obter_doacao(self, donation_id: int) -> Donation:
        """Busca uma doação pelo ID cadastrado."""
        if donation_id not in self._donations:
            raise KeyError(f"Doação com ID {donation_id} não encontrada.")
        return self._donations[donation_id]

    def listar_por_doador(self, donor_id: int, status: Optional[str] = None) -> List[Donation]:
        """Filtra o histórico de doações realizadas por um doador."""
        doacoes = [d for d in self._donations.values() if d.donor_id == donor_id]
        if status:
            doacoes = [d for d in doacoes if d.status == status]
        return doacoes

    def listar_por_instituicao(self, institution_id: int, status: Optional[str] = None) -> List[Donation]:
        """Filtra as doações destinadas a uma instituição específica."""
        doacoes = [d for d in self._donations.values() if d.institution_id == institution_id]
        if status:
            doacoes = [d for d in doacoes if d.status == status]
        return doacoes

    def _extrair_e_validar_donor(self, donor: Union[Donor, User, int]) -> int:
        if isinstance(donor, int):
            if donor <= 0:
                raise ValueError("ID do doador deve ser maior que zero.")
            return donor
        if isinstance(donor, (Donor, User)):
            if getattr(donor, "user_type", None) != "donor":
                raise ValueError("O usuário informado não possui perfil de doador (donor).")
            return getattr(donor, "user_id", None) or 1
        raise ValueError("Doador deve ser uma instância de Donor ou um ID inteiro válido.")

    def _extrair_e_validar_institution(self, inst: Union[Institution, User, int]) -> int:
        if isinstance(inst, int):
            if inst <= 0:
                raise ValueError("ID da instituição deve ser maior que zero.")
            return inst
        if isinstance(inst, (Institution, User)):
            if getattr(inst, "user_type", None) != "institution":
                raise ValueError("O usuário informado não possui perfil de instituição (institution).")
            return getattr(inst, "user_id", None) or 1
        raise ValueError("Instituição deve ser uma instância de Institution ou um ID inteiro válido.")
