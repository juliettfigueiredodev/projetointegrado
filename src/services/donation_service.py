# Lógica de realizar doação
class DonationService:
    def realizar_doacao(self, donor, institution, amount):
        # Lógica para processar a doação
        print(f"Doação de R${amount} realizada por {donor.donor_name} para {institution.institution_name}.")
        