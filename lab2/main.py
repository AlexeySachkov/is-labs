from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from Client import Client
from TicketSaler import TicketSaler
from FoodSaler import FoodSaler
if __name__ == '__main__':

    agents = list()
    port = 4004
    client = Client(AID(name='client@localhost:{}'.format(port)))
    agents.append(client)

    port += 1
    foodSaler = FoodSaler(AID(name='food_saler@localhost:{}'.format(port)))
    agents.append(foodSaler)

    port += 1
    ticketSaler = TicketSaler(AID(name='ticket_saler@localhost:{}'.format(port)))
    agents.append(ticketSaler)
    start_loop(agents)
