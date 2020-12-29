import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID




class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.price = int(random.randint(3000, 5000))
        self.type_room = ['C-Max', 'EcoSport', 'Edge', 'Expedition']

    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Здравствуйте!")
            display_message(self.aid.localname, "У вас есть автомобили в наличии?")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="agent_auto@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            if not flag :
                random_number = int(random.randint(0, 3))
                random_type = self.type_room[random_number]
                display_message(self.aid.localname, "Я хочу приобрести автомобиль {}".format(random_type))
                display_message(self.aid.localname, "Интересуют предложения на сумму {}$".format(self.price))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'price': 0}))
                message.add_receiver(AID(name="agent_auto@localhost:8022"))
                self.send(message)
            else:
                price = content['price']
                if self.price >= price:
                    display_message(self.aid.localname, "Покупаю, вот деньги")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'price': price}))
                    message.add_receiver(AID(name="agent_auto@localhost:8022"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "Слишком дорого")
                    display_message(self.aid.localname, "У меня только {}$".format(self.price))
                    message = ACLMessage()
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'price': self.price}))
                    message.add_receiver(AID(name="agent_auto@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Спасибо, досвидания")



class Auto(Agent):
    def __init__(self, aid):
        super(Auto, self).__init__(aid=aid, debug=False)
        self.type_room = ['C-Max', 'EcoSport', 'Edge', 'Expedition']
        self.type = ''

    def calculate_price(self):
        if self.type == "C-Max":
            return int(random.randint(3000, 3500))
        elif self.type == "EcoSport":
            return int(random.randint(3500, 4000))
        elif self.type == "Edge":
            return int(random.randint(4000, 4500))
        elif self.type == "Expedition":
            return int(random.randint(4500, 5000))

    def min_price(self):
        if self.type == "C-Max":
            return 3000
        elif self.type == "EcoSport":
            return 3500
        elif self.type == "Edge":
            return 4000
        elif self.type == "Expedition":
            return 4500

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Здравствуйте, вам помочь в подборе автомобиля?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_client@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Auto, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Да, какой автомобиль вас интересует?")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'flag': False}))
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            if price == 0:
                self.type = content['type']
                price = self.calculate_price()
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                display_message(self.aid.localname, "Данный автомобиль стоит {}$".format(price))
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Вот ваши ключи")
                display_message(self.aid.localname, "Всего хорошего")
                display_message(self.aid.localname, "Клиент получил ключи от автомобиля {}".format(self.type))

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            min_price = self.min_price()
            if min_price <= price:
                display_message(self.aid.localname, "Мы можем вам предложить спецпредложение")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Извините, мы не можем для вас снизить цену")
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)


if __name__ == '__main__':
    agents = list()

    agent_name = 'agent_client@localhost:8011'
    agent_client = Client(AID(name=agent_name))
    agent_auto = Auto(AID(name="agent_auto@localhost:8022"))

    agents.append(agent_client)
    agents.append(agent_auto)


    start_loop(agents)