from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

class TicketSaler(Agent):

		
    def __init__(self, aid):
        self.ticketPrice = 150 
        self.wealth = 0
        super(TicketSaler, self).__init__(aid=aid, debug=False)


    def react(self, message):
        super(TicketSaler, self).react(message)
        
        sender_name = message.sender.name.split('@')[0]
        if sender_name == "client":

                display_message(self.aid.localname, 'Message received from {}'.format(message.sender.name.split('@')))
                
                if message.content == "I need to buy a ticket. What is the price?":
                        data = self.ticketPrice
                        self.sending_message(data)
                elif message.content == "Here is the money?":
                        data = "Thank You"
                        self.wealth = self.ticketPrice
                        self.ticketPrice = 0
                        self.sending_message(data)

   
    def sending_message(self,content):
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('client'))
        message.set_content(content)
        self.send(message)
