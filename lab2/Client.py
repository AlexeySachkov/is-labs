from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID


class Client(Agent):

    def __init__(self, aid):

        self.clientWealth = 500
        self.ticketPrice = 0
        self.foodPrice = 0
        super(Client, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, 'Here is Client. He has '+str(self.clientWealth))

    def on_start(self):
        super(Client, self).on_start()
        display_message(self.aid.localname, 'sending Message...')
				
        call_later(8.0, self.asking_ticket_price)
        call_later(10.0, self.buy_the_ticket)
        call_later(12.0, self.asking_food_price)
        call_later(14.0, self.buy_the_food)

    def asking_ticket_price(self):
        display_message(self.aid.localname, 'Going to meet ticket saler')
        msg = "I need to buy the ticket. What is the price?"
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('ticket_saler'))
        message.set_content(msg)
        self.send(message)

    def asking_food_price(self):

        display_message(self.aid.localname, 'Going to the food saler')
        msg = "I need to buy the popcorn and pepsi. What is the price?"
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('food_saler'))
        message.set_content(msg)
        self.send(message)

    def buy_the_food(self):
        
        display_message(self.aid.localname, 'Giving money to the food saler')
        msg = "Here is the money?"
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('food_saler'))
        message.set_content(msg)
        self.send(message)


    def buy_the_ticket(self):

        display_message(self.aid.localname, 'Giving money to the ticket saler')
        msg = "Here is the money?"
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('ticket_saler'))
        message.set_content(msg)
        self.send(message)

    def react(self, message):
        super(Client, self).react(message)
        
        if (message.sender.name.split('@')[0]=="ticket_saler"):

            display_message(self.aid.localname, 'Message received from {}'.format(message.sender.name.split('@')))

            print("Msg from Ticket Saler = ",message.content)
            if message.content == "Thank You" :
                self.clientWealth -= self.ticketPrice
                display_message(self.aid.localname, "I bought the ticket")
        			
            else:
                self.ticketPrice = message.content 
                print("Ticket price is ",message.content )
                display_message(self.aid.localname, "I'm going to buy the ticket")

        elif (message.sender.name.split('@')[0]=="food_saler"):

            display_message(self.aid.localname, 'Message received from {}'.format(message.sender.name.split('@')))
            
            print("Msg from Food Saler = ",message.content)
            if message.content == "Thank You" :
                self.clientWealth -= self.foodPrice
                display_message(self.aid.localname, "I bought the popcorn and pepsi")
            		
            else:
                self.foodPrice = message.content 
                print("Food price is ",message.content )
                display_message(self.aid.localname, "I'm going to buy the popcorn and pepsi")
