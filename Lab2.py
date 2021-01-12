
# Доставка.
# Клиент решил оформить доставку от ресторана и одновременно с этим узнать способ доставки и стоимость.
# Operator - оператор доставки.
# Client - клиент доставки.


import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

class Operator(Agent):
    def __init__(self, aid):
        super(Operator, self).__init__(aid=aid, debug=False)
        self.type = ['Пеший курьер', 'Вело курьер', 'Авто курьер']

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Добрый день.")
        display_message(self.aid.localname, "Как далеко вы находитесь от ресторана?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="client@localhost:7000"))
        self.send(message)

    def react(self, message):
        super(Operator, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            choose = content['km']
            if choose == '3km' or '2km' or '1km':
                self.type_one = self.type[0]
                self.type_two = self.type[1]
                self.type_three = self.type[2]

            message = ACLMessage()
            display_message(self.aid.localname, "Доступен: {}.".format(self.type_one))
            display_message(self.aid.localname, "Доступен: {}.".format(self.type_two))
            display_message(self.aid.localname, "Доступен: {}.".format(self.type_three))

            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps(
                {'type_one': self.type_one, 'type_two': self.type_two, 'type_three': self.type_three, 'selected_type_delivery': False}))
            message.add_receiver(AID(name="client@localhost:7000"))
            self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            if not price:
                self.price_one = random.randint(100, 250)
                self.price_two = random.randint(120, 270)
                self.price_three = random.randint(140, 290)
                message = ACLMessage()
                display_message(self.aid.localname, "Стоимость доставки составит: {}:00.".format(self.price_one))
                display_message(self.aid.localname, "Стоимость доставки составит: {}:00.".format(self.price_two))
                display_message(self.aid.localname, "Стоимость доставки составит: {}:00.".format(self.price_three))
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps(
                    {'price_one': self.price_one, 'price_two': self.price_two, 'price_three': self.price_three,
                     'selected_type_delivery': True}))
                message.add_receiver(AID(name="client@localhost:7000"))
                self.send(message)

            else:
                display_message(self.aid.localname, "Заказ оформлен!")
                display_message(self.aid.localname, "Ожидайте курьера в указанное время.")
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="client@localhost:7000"))
                self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Очень жаль, что не сможем доставить вам заказ.")
            display_message(self.aid.localname, "Надеемся, что вы снова захотите воспользоваться нашим сервисом.")
            message = ACLMessage()
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name="client@localhost:7000"))
            self.send(message)


class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.km = ['3km', '2km', '1km']
        self.type = ['Пеший курьер', 'Вело курьер', 'Авто курьер']

    def react(self, message):
        super(Client, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            self.rand_km = self.km[random.randint(0, 2)]
            message = ACLMessage()
            display_message(self.aid.localname, "Здравствуйте.")
            display_message(self.aid.localname, "Я нахожусь от ресторана в {}.".format(self.rand_km))
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'km': self.rand_km}))
            message.add_receiver(AID(name="operator@localhost:7500"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            self.selected_type = content['selected_type_delivery']
            if not self.selected_type:
                self.suitable = random.randint(0, 1)
                message = ACLMessage()
                if self.suitable == 1:
                    self.able_type = [content['type_one'], content['type_two'], content['type_three']]
                    self.rand_suit_type = self.able_type[random.randint(0, 2)]
                    display_message(self.aid.localname, "Мне подходит {}.".format(self.rand_suit_type))
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'suit_type': self.rand_suit_type, 'price': False}))
                else:
                    display_message(self.aid.localname, "Мне не подходят данные типы доставки. Всего доброго.")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="operator@localhost:7500"))
                self.send(message)
            else:
                self.suitable = random.randint(0, 1)
                message = ACLMessage()
                if self.suitable == 1:
                    self.able_price = [content['price_one'], content['price_two'], content['price_three']]
                    self.rand_suit_price = self.able_price[random.randint(0, 2)]
                    display_message(self.aid.localname, "Давайте остановимся на {}:00.".format(self.rand_suit_price))
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'price': True}))
                else:
                    display_message(self.aid.localname, "К сожалению мне не подходит итоговая сумма. Всего доброго.")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="operator@localhost:7500"))
                self.send(message)


if __name__ == '__main__':
    agents = list()
    client = Client(AID(name='client@localhost:7000'))
    operator = Operator(AID(name="operator@localhost:7500"))
    agents.append(client)
    agents.append(operator)
    start_loop(agents)
