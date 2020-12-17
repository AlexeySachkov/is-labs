import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID




class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.price = int(random.randint(400, 600))
        self.type_pizza = ['Студенческая', 'С ветчиной и грибами', '4 сыра', 'Маргарита']

    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Здравствуйте, я бы хотел заказать пиццу")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="agent_pizza@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            if not flag :
                random_number = int(random.randint(0, 3))
                random_type = self.type_pizza[random_number]
                display_message(self.aid.localname, "Я хочу пиццу {}".format(random_type))
                display_message(self.aid.localname, "У меня есть {}".format(self.price))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'price': 0}))
                message.add_receiver(AID(name="agent_pizza@localhost:8022"))
                self.send(message)
            else:
                price = content['price']
                if self.price >= price:
                    display_message(self.aid.localname, "Покупаю, вот деньги")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'price': price}))
                    message.add_receiver(AID(name="agent_pizza@localhost:8022"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "Слишком дорого")
                    display_message(self.aid.localname, "У меня только {}".format(self.price))
                    message = ACLMessage()
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'price': self.price}))
                    message.add_receiver(AID(name="agent_pizza@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Спасибо, досвидания")



class Pizza(Agent):
    def __init__(self, aid):
        super(Pizza, self).__init__(aid=aid, debug=False)
        self.type_pizza = ['Студенческая', 'С ветчиной и грибами', '4 сыра', 'Маргарита']
        self.type = ''

    def calculate_price(self):
        if self.type == "Студенческая":
            return int(random.randint(400, 450))
        elif self.type == "С ветчиной и грибами":
            return int(random.randint(450, 500))
        elif self.type == "4 сыра":
            return int(random.randint(500, 550))
        elif self.type == "Маргарита":
            return int(random.randint(550, 600))

    def min_price(self):
        if self.type == "Студенческая":
            return 400
        elif self.type == "С ветчиной и грибами":
            return 450
        elif self.type == "4 сыра":
            return 500
        elif self.type == "Маргарита":
            return 550

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Здравствуйте, что будете заказывать ?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_client@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Pizza, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Да, какую пиццу будете ?")
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
                display_message(self.aid.localname, "С вас {}".format(price))
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Вот ваша пицца")
                display_message(self.aid.localname, "Всего хорошего")

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            min_price = self.min_price()
            if min_price <= price:
                display_message(self.aid.localname, "Мы можем вам пиццу по акции")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Извините, мы не можем продать дешевле")
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)


if __name__ == '__main__':
    agents = list()

    agent_name = 'agent_client@localhost:8011'
    agent_client = Client(AID(name=agent_name))
    agent_pizza = Pizza(AID(name="agent_pizza@localhost:8022"))

    agents.append(agent_client)
    agents.append(agent_pizza)


    start_loop(agents)