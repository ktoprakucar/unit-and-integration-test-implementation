from src.service.organization_service import OrganizationService
from src.service.ticket_service import TicketService


class ConcertService:

    def __init__(self):
        self.__organization_service = OrganizationService()
        self.__ticket_service = TicketService()

    def organize_concert(self):
        band: str = self.__organization_service.choose_band()
        ticket_price: int = self.__ticket_service.define_ticket_price(band)
        return {'band': band,
                'ticket_price': ticket_price}
