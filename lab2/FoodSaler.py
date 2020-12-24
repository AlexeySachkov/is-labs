from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

class FoodSaler(Agent):

		
    def __init__(self, aid):
        self.popcornPrice = 50
        self.pepsiPrice = 25
        self.wealth = 0
        super(FoodSaler, self).__init__(aid=aid, debug=False)


    def react(self, message):
        super(FoodSaler, self).react(message)
        
        sender_name = message.sender.name.split('@')[0]
        if sender_name == "client":

            display_message(self.aid.localname, 'Message received from {}'.format(message.sender.name.split('@')))
            
            if message.content == "I need to buy the popcorn and pepsi. What is the price?":
                data = self.popcornPrice + self.pepsiPrice
                self.sending_message(data)
            elif message.content == "Here is the money?":
                data = "Thank You"
                self.wealth = self.popcornPrice + self.pepsiPrice
                self.popcornPrice = 0
                self.pepsiPrice = 0
                self.sending_message(data)

   
    def sending_message(self,content):
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('client'))
        message.set_content(content)
        self.send(message)
