import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.quantity = int(random.randint(3, 18))
        self.product_list = ['Tomat', 'Potatoes', 'Cucumber', 'Cabbage' , 'Onion']
        self.discount = int(random.randint(5, 15))
		
    def react(self, message):
        super(Client, self).react(message)
        random_element = int(random.randint(0, 3))
        random_type = self.product_list[random_element]

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Hello!")
            display_message(self.aid.localname, "I want to buy vegetables")
            display_message(self.aid.localname, "What can you suggest?")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="seller@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            accept = content['accept']
            if not flag :
                display_message(self.aid.localname, "I want to buy {} ".format(random_type))
                display_message(self.aid.localname, "in quantity {} ".format(self.quantity))
                display_message(self.aid.localname, "Do you have that much?")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'quantity': 0,'discount': 0}))
                message.add_receiver(AID(name="seller@localhost:8022"))
                self.send(message)
            else:
                quantity = content['quantity']
                if self.quantity <= quantity:
                    display_message(self.aid.localname, "This option suits me ")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    display_message(self.aid.localname, "Can you provide a discount at {} %".format(self.discount))
                    message.set_content(json.dumps({'type': random_type,'quantity': self.quantity, 'discount': self.discount}))
                    message.add_receiver(AID(name="seller@localhost:8022"))
                    self.send(message)
                else:
                    if not accept:   
                        display_message(self.aid.localname, "So no good")
                        display_message(self.aid.localname, "I need {}".format(self.quantity))
                        message = ACLMessage()
                        message.set_performative(ACLMessage.REJECT_PROPOSAL)
                        message.set_content(json.dumps({'quantity': self.quantity}))
                        message.add_receiver(AID(name="seller@localhost:8022"))
                        self.send(message)
                    else:
                        if self.quantity - 1 <= quantity:
                            display_message(self.aid.localname, "This option suits me ")
                            message = ACLMessage()
                            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                            display_message(self.aid.localname, "Can you provide a discount at {} % ".format(self.discount))
                            message.set_content(json.dumps({'type': random_type, 'quantity': quantity, 'discount': self.discount}))
                            message.add_receiver(AID(name="seller@localhost:8022"))
                            self.send(message)
                        else:
                            display_message(self.aid.localname, "I do not like it ")
                            message = ACLMessage()
                            message.set_performative(ACLMessage.REJECT_PROPOSAL)
                            message.set_content(json.dumps({'accept': False, 'quantity': self.quantity}))
                            message.add_receiver(AID(name="seller@localhost:8022"))
                            self.send(message)

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            reject = content['reject']
            quantity = content['quantity']
            if reject == True:
                display_message(self.aid.localname, "Thank you,bye")
            else:
                display_message(self.aid.localname, "Ok")
                self.discount = self.discount/2
                display_message(self.aid.localname, "Can you provide a discount at {} %".format(self.discount))
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'quantity': quantity, 'discount': self.discount}))
                message.add_receiver(AID(name="seller@localhost:8022"))
                self.send(message)

class Seller(Agent):
    def __init__(self, aid):
        super(Seller, self).__init__(aid=aid, debug=False)
        self.product_list = ['Tomat', 'Potatoes', 'Cucumber', 'Cabbage' , 'Onion']
        self.quantity = 0
        self.type = ''

    def calculate_price(self):
        if self.type == "Tomat":
            return int(random.randint(80, 100))
        elif self.type == "Potatoes":
            return int(random.randint(30, 50))
        elif self.type == "Cucumber":
            return int(random.randint(45, 60))
        elif self.type == "Cabbage":
            return int(random.randint(20, 40))
        elif self.type == "Onion":    
            return int(random.randint(15, 35))

    def min_price(self):
        if self.type == "Tomat":
            return 80
        elif self.type == "Potatoes":
            return 30
        elif self.type == "Cucumber":
            return 45
        elif self.type == "Cabbage":
            return 20
        elif self.type == "Onion":
            return 15

    def available_quantity(self):
        if self.type == "Tomat":
            return int(random.randint(10, 15))
        elif self.type == "Potatoes":
            return int(random.randint(5, 10))
        elif self.type == "Cucumber":
            return int(random.randint(5, 10))
        elif self.type == "Cabbage":
            return int(random.randint(10, 15))
        elif self.type == "Onion":    
            return int(random.randint(5, 10))

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="client@localhost:8011"))
        self.send(message)
	
    def react(self, message):
        super(Seller, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "We have:Tomat,Potatoes,Cucumber,Cabbage,Onion")
            display_message(self.aid.localname, "What have you chosen?")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'flag': False,'accept': False}))
            message.add_receiver(AID(name="client@localhost:8011"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            quantity = content['quantity']
            discount = content['discount']
            self.type = content['type']
            if quantity == 0 and discount ==0:
                quantity = self.available_quantity()
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                display_message(self.aid.localname, "Now, i have {}".format(quantity))
                message.set_content(json.dumps({'flag': True, 'quantity': quantity, 'accept': True}))
                message.add_receiver(AID(name="client@localhost:8011"))
                self.send(message)
            elif quantity!=0 and discount!=0:
                price = self.calculate_price() * quantity
                minprice=self.min_price() * quantity
                disc_price=price - ((price / 100) * discount)
                if disc_price >= minprice:
                    display_message(self.aid.localname, "Ok")
                    self.quantity=quantity
                    display_message(self.aid.localname, "Sales {} kg".format(self.quantity))
                    display_message(self.aid.localname, "Amount without discount {}".format(price))
                    display_message(self.aid.localname, "Total amount  {}".format(disc_price))
                else: 
                    display_message(self.aid.localname, "Sorry I can't help you then")
                    message = ACLMessage()
                    message.set_content(json.dumps({'reject': False,'quantity': quantity}))
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="client@localhost:8011"))
                    self.send(message)

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            quantity = content['quantity']
            accept = content['accept']
            min_quantity = self.available_quantity()
            if accept != False:
                if min_quantity <= quantity:
                    display_message(self.aid.localname, "I can't sell more than {}".format(quantity))
                    display_message(self.aid.localname, "Will that suit you?")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'flag': True, 'quantity': quantity, 'accept': True}))
                    message.add_receiver(AID(name="client@localhost:8011"))
                    self.send(message)
            else:
                display_message(self.aid.localname, "Sorry I can't help you then")
                message = ACLMessage()
                message.set_content(json.dumps({'reject': True,'quantity': quantity}))
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="client@localhost:8011"))
                self.send(message)


if __name__ == '__main__':
    agents = list()

    agent_client = Client(AID(name="client@localhost:8011"))
    agent_seller = Seller(AID(name="seller@localhost:8022"))

    agents.append(agent_client)
    agents.append(agent_seller)


    start_loop(agents) 