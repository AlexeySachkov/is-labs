import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID


class Broker1(Agent):
    def __init__(self, aid):
        super(Broker1, self).__init__(aid=aid, debug=False)
        self.max_price = 160
        self.min_price = 140

    def react(self, message):
        super(Broker1, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            price = int(content['price'])
            display_message(self.aid.localname, "Цена лота: {}".format(price))
            message = ACLMessage()
            if price < self.min_price:
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name='agent_rialto@localhost:8011'))
                display_message(self.aid.localname, "Брокер1: Поднять")
                self.send(message)
            elif self.min_price <= price <= self.max_price:
                message = ACLMessage()
                message.set_performative(ACLMessage.PROPOSE)
                message.set_content(price)
                message.add_receiver(AID(name="agent_client@localhost:8033"))
                self.send(message)
                display_message(self.aid.localname, "Запрос клиенту...")
            elif price > self.max_price:
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name='agent_rialto@localhost:8011'))
                display_message(self.aid.localname, "Брокер1: Не участвовать")
                self.send(message)


class Auction(Agent):
    def __init__(self, aid):
        super(Auction, self).__init__(aid=aid, debug=False)
        self.counter = 0
        self.price = random.randint(125, 200)

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Лот открыт")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'price': self.price}))
        message.add_receiver(AID(name="agent_broker@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(Auction, self).react(message)

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            self.price = random.randint(125, 200)
            self.send_proposal()


class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.maximum_price = 155
        self.min_price = 140

    def react(self, message):
        super(Client, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = message.content
            price = content
            display_message(self.aid.localname, "Лот стоимостью {}".format(price))
            display_message(self.aid.localname, "Решение клиента:")
            message = ACLMessage()
            if self.min_price <= price <= self.maximum_price:
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name='agent_broker@localhost:8022'))
                display_message(self.aid.localname, "Принять предложение. Завершение торгов")
                self.send(message)
            else:
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name='agent_broker@localhost:8022'))
                display_message(self.aid.localname, "Отказ. Завершение торгов")
                self.send(message)


if __name__ == '__main__':
    agents = list()

    agent_name = 'agent_rialto@localhost:8011'
    agent_hello = Auction(AID(name=agent_name))
    agent2 = Broker1(AID(name="agent_broker@localhost:8022"))
    agent3 = Client(AID(name='agent_client@localhost:8033'))

    agents.append(agent_hello)
    agents.append(agent2)
    agents.append(agent3)

    start_loop(agents)
