from glpipci.comunicator.v10_0.endpoints.tickets.core import GlpiTicket
from glpipci.commons.decorators import debug_print_params

CONTEXT_URI_PATTERN = "/Ticket_User"


class GlpiTicketTicketUserBodyItem:
    def __init__(self, tickets_id, users_id, user_type, use_notification, alternative_email):
        self.tickets_id = tickets_id
        self.users_id = users_id
        self.user_type = user_type
        self.use_notification = use_notification
        self.alternative_email = alternative_email


class GlpiTicketTicketUser:

    def __init__(self, ticket_instance: GlpiTicket) -> None:
        self.ticket_instance = ticket_instance
        self.ticket_user_elements = []

    @debug_print_params
    def get_ticket_users(self) -> list[dict]:
        """
        Get the list of ITIL followups for a ticket.
        """
        endpoint = self.ticket_instance.api_object_endpoint + CONTEXT_URI_PATTERN
        response = self.ticket_instance.api_client.make_get(
            endpoint,
            headers=self.ticket_instance.api_client.auth_headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            self.ticket_instance.api_client.request_error_handler(
                status_code=response.status_code,
                message=response.text
            )

    @debug_print_params
    def add_ticket_users(self, ticket_users_list: list) -> dict:
        """
        Add a new ITIL followup for a ticket.

        TODO: Implement to change from dict to specific class
        """
        endpoint = self.ticket_instance.api_object_endpoint + CONTEXT_URI_PATTERN
        response = self.ticket_instance.api_client.make_post(
            endpoint,
            headers=self.ticket_instance.api_client.auth_headers,
            json={
                "input": ticket_users_list
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            self.ticket_instance.api_client.request_error_handler(
                status_code=response.status_code,
                message=response.text
            )

    # def convert_users_elements(self, ticket_users_list:list[dict]) -> list[GlpiTicketTicketUserBodyItem]:
    #     return [GlpiTicketTicketUserBodyItem(
    #         tickets_id=self.ticket_instance.ticket_id,
    #         users_id=el.get("users_id", "0"),
    #         user_type=el.get("user_type", "1"),
    #         use_notification=el.get("use_notification", "0"),
    #         alternative_email=el.get("alternative_email", "")
    #     ) for el in ticket_users_list ]