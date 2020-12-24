import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID




class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.money = int(random.randint(100, 300))
        self.type_room = ['эконом', 'стандарт', 'люкс', 'президентский']

    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Здравствуйте!")
            display_message(self.aid.localname, "У вас есть номер?")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="agent_hotel@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            if not flag :
                random_number = int(random.randint(0, 3))
                random_type = self.type_room[random_number]
                display_message(self.aid.localname, "Я хочу номер {} номер".format(random_type))
                display_message(self.aid.localname, "У меня есть {}".format(self.price))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'price': 0}))
                message.add_receiver(AID(name="agent_hotel@localhost:8022"))
                self.send(message)
            else:
                price = content['price']
                if self.price >= price:
                    display_message(self.aid.localname, "Покупаю, вот деньги")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'price': price}))
                    message.add_receiver(AID(name="agent_hotel@localhost:8022"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "Слишком дорого")
                    display_message(self.aid.localname, "У меня только {}".format(self.price))
                    message = ACLMessage()
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'price': self.price}))
                    message.add_receiver(AID(name="agent_hotel@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Спасибо, досвидания")



class Hotel(Agent):
    def __init__(self, aid):
        super(Hotel, self).__init__(aid=aid, debug=False)
        self.type_room = ['эконом', 'стандарт', 'люкс', 'президентский']
        self.type = ''

    def calculate_price(self):
        if self.type == "эконом":
            return int(random.randint(100, 120))
        elif self.type == "стандарт":
            return int(random.randint(120, 140))
        elif self.type == "люкс":
            return int(random.randint(140, 160))
        elif self.type == "президентский":
            return int(random.randint(200, 300))

    def min_price(self):
        if self.type == "эконом":
            return 100
        elif self.type == "стандарт":
            return 120
        elif self.type == "люкс":
            return 140
        elif self.type == "президентский":
            return 200

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Добрый день! Вам помочь?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_client@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Hotel, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Да, какой хотите?")
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
                display_message(self.aid.localname, "Он стоит {}".format(price))
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Гостиница получила {}".format(price))
                display_message(self.aid.localname, "Вот ваши ключи")
                display_message(self.aid.localname, "Всего хорошего")

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            min_price = self.min_price()
            if min_price <= price:
                display_message(self.aid.localname, "Мы можем для вас снизить цену")
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
    agent_hotel = Hotel(AID(name="agent_hotel@localhost:8022"))

    agents.append(agent_client)
    agents.append(agent_hotel)


    start_loop(agents)

    
#[agent_hotel] 23/12/2020 18:08:11.991 --> Добрый день! Вам помочь?
#[agent_client] 23/12/2020 18:08:13.478 --> Здравствуйте!
#[agent_client] 23/12/2020 18:08:13.480 --> У вас есть номер?
#[agent_hotel] 23/12/2020 18:08:13.490 --> Да, какой хотите?
#[agent_client] 23/12/2020 18:08:13.499 --> Я хочу номер стандарт номер
#[agent_client] 23/12/2020 18:08:13.500 --> У меня есть 268
#[agent_hotel] 23/12/2020 18:08:13.511 --> Он стоит 139
#[agent_client] 23/12/2020 18:08:13.516 --> Покупаю, вот деньги
#[agent_hotel] 23/12/2020 18:08:13.521 --> Гостиница получила 139
#[agent_hotel] 23/12/2020 18:08:13.521 --> Вот ваши ключи
#[agent_hotel] 23/12/2020 18:08:13.522 --> Всего хорошего
