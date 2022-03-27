class TicketService:

    def define_ticket_price(self, band: str) -> int:
        if len(band) > 5:
            return 10
        else:
            return 20
