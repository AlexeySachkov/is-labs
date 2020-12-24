# 3 агента клиент, официант, повар
# Клиент приходит ресторан, где заказывал столик
# Клиент смотрит меню и выбриает 1-2 блюда японской кухни или
# 1-2 блюда итальянской кухни , также 1-2 десерта.
# Клиент вызывает официанта и говорит заказ
# С этим заказом официант идет к повару.
# Повар готовит заказ. И после отдает заказ официанту.
# Официант отдает заказ клиенту.
# Клиент либо доволен всем и все понравилось.
# В этом случае официант говорит повару, что все отлично
# Если клиент не доволен, то заведение не берет денег за то блюдо,
# которое не понравилось клиенту.
# После этого клиент идет к повару и говорит, что клиенту это блюдо не порнавилось
# На что повар говорит, что он это блюдо улучшит, чтоб оно понравилось всем!


import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID


class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.price = 1000
        self.order = []
        self.orderPrice = 0

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Здравствуйте! Я заказывал столик.")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'chose': False}))
        message.add_receiver(AID(name="agent_waiter@localhost:8022"))
        self.send(message)

    def random_order(self, menu):
        numberOFcuisine = random.randint(0, 1)
        numberOFfood = random.randint(1, 2)
        numberOFdessert = random.randint(1, 2)
        i = 0
        if numberOFcuisine == 0:
            while (i < numberOFfood) and (self.orderPrice <= self.price):
                number = random.randint(0, len(menu['Японская кухня']) - 1)
                if not (menu['Японская кухня'][number][0] in self.order):
                    self.order.append(menu['Японская кухня'][number][0])
                    self.orderPrice += menu['Японская кухня'][number][1]
                    i += 1

        elif numberOFcuisine == 1:
            while (i < numberOFfood) and (self.orderPrice <= self.price):
                number = random.randint(0, len(menu['Итальянская кухня']) - 1)
                if not (menu['Итальянская кухня'][number][0] in self.order):
                    self.order.append(menu['Итальянская кухня'][number][0])
                    self.orderPrice += menu['Итальянская кухня'][number][1]
                    i += 1

        i = 0
        while (i < numberOFdessert) and (self.orderPrice <= self.price):
            number = random.randint(0, len(menu['Десерты']) - 1)
            if not (menu['Десерты'][number][0] in self.order):
                self.order.append(menu['Десерты'][number][0])
                self.orderPrice += menu['Десерты'][number][1]
                i += 1

        if self.orderPrice > self.price:
            self.order.pop(len(self.order) - 1)


    def react(self, message):
        super(Client, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Клиент вызывает оффицианта")
            content = json.loads(message.content)
            menu = content['menu']
            self.random_order(menu)
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'chose': True}))
            message.add_receiver(AID(name="agent_waiter@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            ready = content['ready']
            if ready:
                display_message(self.aid.localname, "Заказ принял клиент")
                message = ACLMessage()
                number = random.randint(0, 1)
                if number == 1:
                    number = random.randint(0, len(self.order) - 1)
                    display_message(self.aid.localname, "Мне не понравилось это блюдо: {}".format(self.order[number]))
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'type': self.order[number], "price": self.price}))
                    message.add_receiver(AID(name="agent_waiter@localhost:8022"))
                    self.send(message)
                elif number == 0:
                    display_message(self.aid.localname, "Мне все очень понравилось!")
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({"price": self.orderPrice, 'name': 'Client'}))
                    message.add_receiver(AID(name="agent_waiter@localhost:8022"))
                    self.send(message)
            else:
                display_message(self.aid.localname, "Да")
                display_message(self.aid.localname, "Мне пожалуйста это: {}".format(self.order))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'order': self.order, 'name': 'Client', 'price': 0}))
                message.add_receiver(AID(name="agent_waiter@localhost:8022"))
                self.send(message)

class Waiter(Agent):
    def __init__(self, aid):
        super(Waiter, self).__init__(aid=aid, debug=False)
        self.menu = { 'Японская кухня':     [['Калифорния', 240], ['Филадельфия', 310],
                                            ['Аляска', 210], ['Канада', 280],
                                            ['Рамен', 190], ['Хофу', 290]],
                      'Итальянская кухня':  [['Ризотто', 380], ['Спагетти Карбонара', 310],
                                            ['Лазанья', 295], ['Суп Минестроне', 225]],
                      'Десерты':            [['Медовик', 140], ['яблочный Штрудель', 245],
                                            ['Чизкейк', 235], ['Торт Ченси', 195],
                                            ['Тирамису', 220]]
                    }

    def cost_search(self, type):
        for i in self.menu:
            for j in self.menu[i]:
                if j[0] == type:
                    return j[1]


    def react(self, message):
        super(Waiter, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            chose = content['chose']
            if chose:
                display_message(self.aid.localname, "Что будете заказывать?")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'ready': False}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Добрый день! Да, прошу к 3 столику.")
                message = ACLMessage()
                message.set_performative(ACLMessage.PROPOSE)
                message.set_content(json.dumps({'menu': self.menu}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            name = content['name']
            if name == 'Client':
                price = content['price']
                if price == 0:
                    order = content['order']
                    display_message(self.aid.localname, "Спасибо за заказ! Ожидайте")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.PROPOSE)
                    message.set_content(json.dumps({'order': order}))
                    message.add_receiver(AID(name="agent_cook@localhost:8033"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "Официант получил {} монет".format(price))
                    display_message(self.aid.localname, "Спасибо, приходите ищё!")
                    display_message(self.aid.localname, "Относит посуду")
                    display_message(self.aid.localname, "Клиенту все понравилось")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.add_receiver(AID(name="agent_cook@localhost:8033"))
                    self.send(message)

            elif name == 'Cook':
                order = content['order']
                display_message(self.aid.localname, "Официант принял заказ от повара")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'order': order, 'ready': True}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            type = content['type']
            price = content['price']
            display_message(self.aid.localname, "Приносим извинения за это блюдо {}".format(type))
            display_message(self.aid.localname, "В качестве извинений, можете за это блюдо не платить")
            cost = self.cost_search(type)
            price = price - cost
            display_message(self.aid.localname, "Официант получил {} монет".format(price))
            display_message(self.aid.localname, "Спасибо, приходите ищё!")
            display_message(self.aid.localname, "Относит посуду")
            display_message(self.aid.localname, "Клиенту не понравилось это блюдо {}".format(type))
            message = ACLMessage()
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.set_content(json.dumps({'type': type}))
            message.add_receiver(AID(name="agent_cook@localhost:8033"))
            self.send(message)




class Cook(Agent):
    def __init__(self, aid):
        super(Cook, self).__init__(aid=aid, debug=False)

    def react(self, message):
        super(Cook, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            order = content['order']
            display_message(self.aid.localname, "Повар принял заказ от официанта")
            for i in range(random.randint(1, 10)):
                display_message(self.aid.localname, "Повар готовит...")
            display_message(self.aid.localname, "Повар приготовил!")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'order': order, 'name': 'Cook'}))
            message.add_receiver(AID(name="agent_waiter@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            display_message(self.aid.localname, "Я рад! Хорошая работа")
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            type = content['type']
            display_message(self.aid.localname, "Я постарюсь улучить это блюдо! {}".format(type))
            display_message(self.aid.localname, "Чтобы {} понравилось всем!".format(type))


if __name__ == '__main__':
    agents = list()


    agent_client = Client(AID(name='agent_client@localhost:8011'))
    agent_waiter = Waiter(AID(name='agent_waiter@localhost:8022'))
    agent_cook = Cook(AID(name="agent_cook@localhost:8033"))


    agents.append(agent_client)
    agents.append(agent_cook)
    agents.append(agent_waiter)


    start_loop(agents)