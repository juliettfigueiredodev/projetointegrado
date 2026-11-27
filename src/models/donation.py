from datetime import datetime
from typing import Optional, Dict, Any


class Donation:
    """Entidade que representa uma doação de materiais escolares."""

    STATUS_PENDENTE = "pendente"
    STATUS_CONFIRMADA = "confirmada"
    STATUS_ENTREGUE = "entregue"
    STATUS_CANCELADA = "cancelada"

    STATUS_VALIDOS = {
        STATUS_PENDENTE,
        STATUS_CONFIRMADA,
        STATUS_ENTREGUE,
        STATUS_CANCELADA,
    }

    def __init__(
        self,
        donation_id: int,
        donor_id: int,
        institution_id: int,
        item: Dict[str, Any],
        quantity: int = 1,
        status: str = STATUS_PENDENTE,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        if status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status '{status}' inválido para a doação.")
        if quantity <= 0:
            raise ValueError("A quantidade doada deve ser maior que zero.")

        self.donation_id = donation_id
        self.donor_id = donor_id
        self.institution_id = institution_id
        self.item = item
        self.quantity = quantity
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "donation_id": self.donation_id,
            "donor_id": self.donor_id,
            "institution_id": self.institution_id,
            "item": self.item,
            "quantity": self.quantity,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
