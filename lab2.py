#Ситуация: клиент хочет заказать быструю даставку пиццы.
#Политика кафе доаставлять меньше за 60 минут,иначе доставка за их счет
#Клиент заказывают пиццу(она выбирается рандомно)
#Кафе присваивает номер заказа и идет приготовление заказа
#случайно генерируется время,в результате чего курьер либо извиняется либо отдает просто заказ и уходит.

import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID


class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.pizza_type = ['Сырная', 'Пепперони', 'Ветчина_и_сыр', 'Додо', 'Ципленок_барбекю']

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        #display_message(self.aid.localname, "Здраствуйте!")
        display_message(self.aid.localname, "Можно сделать заказ?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_cafe@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            message = ACLMessage()
            random_number = int(random.randint(0, 4))
            random_pizza = self.pizza_type[random_number]
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            display_message(self.aid.localname, "Я хочу заказать пиццу {}".format(random_pizza))
            message.set_content(json.dumps({'type_pizza': random_pizza}))
            message.add_receiver(AID(name="agent_cafe@localhost:8022"))
            self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            type_agent = content['type_agent']

            if type_agent == 'Cafe':
                number_order = content['number_order']
                display_message(self.aid.localname, "Здраствуйте! Номер моего заказа {}".format(number_order))
                message = ACLMessage()
                message.set_performative(ACLMessage.PROPOSE)
                message.set_content(json.dumps({'number_order': number_order}))
                message.add_receiver(AID(name="agent_courier@localhost:8033"))
                self.send(message)
            elif type_agent == 'Courier':
                display_message(self.aid.localname, "Спасибо за доставку,всего доброго!")
            

class Cafe(Agent):
    def __init__(self, aid):
        super(Cafe, self).__init__(aid=aid, debug=False)
        self.order = int(random.randint(1, 35))

    def react(self, message):
        super(Cafe, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Здраствуйте!")
            display_message(self.aid.localname, "Да,конечно,что вы желаете?")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            type_pizza = content['type_pizza']
            display_message(self.aid.localname, "Клиент заказал {}".format(type_pizza))
            display_message(self.aid.localname," Спасибо за заказ, ваш номер {}".format(self.order))
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'number_order': self.order, 'type_agent': 'Cafe'}))
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)


class Courier(Agent):
    def __init__(self, aid):
        super(Courier, self).__init__(aid=aid, debug=False)
        self.time = int(random.randint(20, 80))

    def react(self, message):
        super(Courier, self).react(message)

        if message.performative == ACLMessage.PROPOSE:

            content = json.loads(message.content)
            number_order = content['number_order']

            display_message(self.aid.localname, "Здраствуйте!")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)

            if self.time > 60:
                display_message(self.aid.localname, "Простите за задержку, вот ваш заказ {} ,так как заказ более 60 минут, то он совершенно бесплатно! Приятного аппетита! До свидания!".format(number_order))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type_agent': 'Courier'}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Вот ваш заказ, спасибо, до свидания и приятного аппетита!")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type_agent': 'Courier'}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)


if __name__ == '__main__':
    agents = list()

    agent_name = "agent_client@localhost:8011"
    agent_client = Client(AID(name=agent_name))
    agent_cafe = Cafe(AID(name="agent_cafe@localhost:8022"))
    agent_courier = Courier(AID(name="agent_courier@localhost:8033"))

    agents.append(agent_client)
    agents.append(agent_cafe)
    agents.append(agent_courier)

    start_loop(agents) 
