#Агент Buyer - покупатель, у которого есть некая сумма денег на покупку недвижимости и на покупку автомобиля.
#Агент LandOwner - владелец недвижимости, который продает ее за фиксированную цену.
#Агент CarSaler - продавец автомобиля, который продает его за фиксированную цену.
#Суть программы заключается в том, что происходит: 
#1) Диалог между агентами Buyer и LandOwner, первый пытается купить недвижимость. 
#2) Диалог между агентами Buyer и CarSaler, первый пытается купить автомобиль.
#3) Если у покупателя на счету больше денег, чем предлагается, то происходит удачная сделка.
#4) Если у покупателя на счету меньше денег, чем предлагается, то сделка не происходит.

import json
import random
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID


class Buyer(Agent):

    def __init__(self, aid):

        self.moneyForLand = random.randint(1000000, 2000000)
        self.moneyForCar = random.randint(800000, 1500000)
        super(Buyer, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, 'Here is Buyer. He has '+str(self.moneyForLand) + ' to buy land and ' + str(self.moneyForCar) + ' to buy car')

    def on_start(self):
        super().on_start()
        self.call_later(10, self.asking_land_price)

    def asking_land_price(self):
        display_message(self.aid.localname, 'Going to meet land owner')
        display_message(self.aid.localname, 'I need to buy the house. What is the price?')
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'price': False}))
        message.add_receiver(AID(name="land_owner@localhost:4002"))
        self.send(message)

    def react(self, message):
        super(Buyer, self).react(message)
        if (message.sender.name.split('@')[0] == "land_owner") & (message.performative == ACLMessage.PROPOSE):
            message = ACLMessage()
            display_message(self.aid.localname, "I have only {}".format(self.moneyForLand))
            message.set_content(json.dumps({'money': self.moneyForLand, 'price': True}))
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name='land_owner@localhost:4002'))
            self.send(message)
        elif (message.sender.name.split('@')[0] == "land_owner") & (message.performative == ACLMessage.ACCEPT_PROPOSAL):
            message = ACLMessage()
            display_message(self.aid.localname, "I'll take it!")
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.add_receiver(AID(name='land_owner@localhost:4002'))
            self.send(message)

            display_message(self.aid.localname, 'Going to meet car saler...')
            message = ACLMessage()
            display_message(self.aid.localname, 'I need to buy the car. What is the price?')
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'price': False}))
            message.add_receiver(AID(name='car_saler@localhost:4001'))
            self.send(message)
           
        elif (message.sender.name.split('@')[0] == "land_owner") & (message.performative == ACLMessage.REJECT_PROPOSAL):
            message = ACLMessage()
            display_message(self.aid.localname, "Sorry for distracting you :(")
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name='land_owner@localhost:4002'))
            self.send(message)

            display_message(self.aid.localname, 'Going to meet car saler...')
            message = ACLMessage()
            display_message(self.aid.localname, 'I need to buy the car. What is the price?')
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'price': False}))
            message.add_receiver(AID(name='car_saler@localhost:4001'))
            self.send(message)
        elif (message.sender.name.split('@')[0] == "car_saler") & (message.performative == ACLMessage.PROPOSE):
            message = ACLMessage()
            display_message(self.aid.localname, "I have only {}".format(self.moneyForCar))
            message.set_content(json.dumps({'money': self.moneyForCar, 'price': True}))
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name='car_saler@localhost:4001'))
            self.send(message)
        elif (message.sender.name.split('@')[0] == "car_saler") & (message.performative == ACLMessage.ACCEPT_PROPOSAL):
            message = ACLMessage()
            display_message(self.aid.localname, "I'll take it!")
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.add_receiver(AID(name='car_saler@localhost:4001'))
            self.send(message)
        elif (message.sender.name.split('@')[0] == "car_saler") & (message.performative == ACLMessage.REJECT_PROPOSAL):
            message = ACLMessage()
            display_message(self.aid.localname, "Sorry for distracting you :(")
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name='car_saler@localhost:4001'))
            self.send(message)


class LandOwner(Agent):

    def __init__(self, aid):
        self.landPrice = 1500000
        self.wealth = 0
        super(LandOwner, self).__init__(aid=aid, debug=False)

    def react(self, message):
        super(LandOwner, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            self.isPrice = content['price']
            message = ACLMessage()
            if not self.isPrice:
                display_message(self.aid.localname, "It costs {}".format(self.landPrice))
                message.set_performative(ACLMessage.PROPOSE)
            else:
                self.moneyForLand = content['money']
                if self.landPrice <= self.moneyForLand:
                    display_message(self.aid.localname, "We are going to sell it to you")
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
                    message = ACLMessage()
                    message.add_receiver(AID(name="buyer@localhost:4000"))
                    display_message(self.aid.localname, "It is good deal")
                    self.send(message)
                elif message.performative == ACLMessage.REJECT_PROPOSAL:
                    message = ACLMessage()
                    display_message(self.aid.localname, "It's ok, dont worry")
                    message.add_receiver(AID(name="buyer@localhost:4000"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "You dont have enough money")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name="buyer@localhost:4000"))
            self.send(message)

          


class CarSaler(Agent):

    def __init__(self, aid):
        self.carPrice = 1200000
        super().__init__(aid=aid, debug=False)

    def react(self, message):
        super(CarSaler, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            self.isPrice = content['price']
            message = ACLMessage()
            if not self.isPrice:
                display_message(self.aid.localname, 'It costs {}'.format(self.carPrice))
                message.set_performative(ACLMessage.PROPOSE)

            else:
                self.moneyForCar = content['money']
                if self.carPrice <= self.moneyForCar:
                    display_message(self.aid.localname, "We are going to sell it to you")
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                else:
                    display_message(self.aid.localname, "You dont have enough money")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name="buyer@localhost:4000"))
            self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            message = ACLMessage()
            message.add_receiver(AID(name="buyer@localhost:4000"))
            display_message(self.aid.localname, "It is good deal")
            self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            message = ACLMessage()
            display_message(self.aid.localname, "It's ok, dont worry")
            message.add_receiver(AID(name="buyer@localhost:4000"))
            self.send(message)


if __name__ == '__main__':

    agents = list()

    buyer = Buyer(AID(name='buyer@localhost:4000'))
    agents.append(buyer)
    carSaler = CarSaler(AID(name='car_saler@localhost:4001'))
    agents.append(carSaler)
    landOwner = LandOwner(AID(name='land_owner@localhost:4002'))
    agents.append(landOwner)
    start_loop(agents)
