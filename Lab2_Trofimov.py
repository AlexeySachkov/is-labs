import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.satiety = ''
        self.money = 1500
        self.order_price = 1500
        self.i_want = ['cыром','картошкой','колбасой',
                       'креветками','курицой','грибами',
                       'перцем','ананасами']
        self.bag = []

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Здравствуйте!")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            name = content['name']
            if name == "Pizzeria":
                display_message(self.aid.localname, "Дайте минутку подумать")
                number = random.randint(0, len(self.i_want) - 1)
                #print(number)
                self.satiety = self.i_want[number]
                display_message(self.aid.localname, "Хочу пиццу с {}".format(self.satiety))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'ingredient': self.i_want[number], 'name': "client", 'price': 0}))
                message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
                self.send(message)
            elif name == "Deliveryman":
                display_message(self.aid.localname, "Спасибо!")
                self.bag = content['bag']
                display_message(self.aid.localname, "Клиент получил {}".format(self.bag))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                money = self.order_price - self.money
                message.set_content(json.dumps({'money': money}))
                message.add_receiver(AID(name="agent_deliveryman@localhost:8033"))
                self.send(message)


        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            price = content['price']
            message = ACLMessage()
            if flag == 0:
                type_pizza = content['type']
                self.satiety = type_pizza
                if self.money >= price:
                    display_message(self.aid.localname, "Звучит заманчиво я покупаю!")
                    display_message(self.aid.localname, "Пиццу {}".format(type_pizza))
                    display_message(self.aid.localname, "По цене {}".format(price))
                    self.money -= price
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'name': "client", 'price': price}))
                    message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
                    self.send(message)
                elif self.money <= price:
                    display_message(self.aid.localname, "У меня не хватает(")
                    display_message(self.aid.localname, "Вы можете дать скидку?(")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'cause': "discount", 'price': price}))
                    message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
                    self.send(message)
            else:
                if self.money >= price:
                    display_message(self.aid.localname, "Огромное спасибо!! Я покупаю")
                    display_message(self.aid.localname, "Пиццу {}".format(self.satiety))
                    display_message(self.aid.localname, "По цене {}".format(price))
                    self.money -= price
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'name': "client", 'price': price}))
                    message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
                    self.send(message)
                elif self.money <= price:
                    display_message(self.aid.localname, "У меня не хватает(")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'cause': "money"}))
                    message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
                    self.send(message)


        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Нет спасибо. Удачного дня!")
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.set_content(json.dumps({'cause': "end"}))
            message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
            self.send(message)


class Pizzeria(Agent):
    def __init__(self, aid):
        super(Pizzeria, self).__init__(aid=aid, debug=False)

        self.menu = {'ЧИЗБЕРРИ': [480, 'cыром'], 'РУССКАЯ': [460,'картошкой'],
                     'ПЕППЕРОНИ': [390,'колбасой'], 'МАЛЕВИЧ': [590,'креветками'], 'КУРИНАЯ': [420,'курицой'],
                     'ГРИБНАЯ': [410,'грибами'], 'БАВАРСКАЯ': [440,'перцем'], 'ГАВАЙСКАЯ': [430,'ананасами']}
        self.order = []
        self.current_pizza = ''

    def pizza_search(self, type):
        for pizza_type in self.menu:
            if type == self.menu[pizza_type][1]:
                result = pizza_type
        return result

    def react(self, message):
        super(Pizzeria, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Добрый день! Вы позвонили в пиццерию. Что желаете заказать?" )
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'name': 'Pizzeria'}))
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            name = content.pop('name')
            message = ACLMessage()
            if name == "client":
                price = content['price']
                if price == 0:
                    ingredient = content['ingredient']
                    self.current_pizza = self.pizza_search(ingredient)
                    display_message(self.aid.localname, "У нас есть пицца с {}".format(ingredient))
                    display_message(self.aid.localname, "Она называется {}".format(self.current_pizza))
                    display_message(self.aid.localname, "Она стоит {}".format(self.menu[self.current_pizza][0]))
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'type': format(ingredient), 'price': self.menu[self.current_pizza][0], 'flag': 0}))
                    message.add_receiver(AID(name="agent_client@localhost:8011"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "Спасибо за покупку, хотите ещё какую-нибудь пиццу?")
                    self.order.append(self.current_pizza)
                    message.set_performative(ACLMessage.PROPOSE)
                    message.set_content(json.dumps({'name': 'Pizzeria'}))
                    message.add_receiver(AID(name="agent_client@localhost:8011"))
                    self.send(message)
            elif name == "Deliveryman":
                money = content['money']
                display_message(self.aid.localname, "Пиццария получила {} монет".format(money))
                display_message(self.aid.localname, "Хорошая работа!")

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            cause = content['cause']
            message = ACLMessage()
            if cause == 'discount':
                price = content['price']
                display_message(self.aid.localname, "Мы можем дать вам скидку 200 монет")
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                changed_price = price - 200
                message.set_content(json.dumps({'price': changed_price, 'flag': 1}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            elif cause == 'money':
                display_message(self.aid.localname, "Желаете что-то ещё?")
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            elif cause == 'end':
                display_message(self.aid.localname, "Досвидания! Спасибо что выбираете нас!")
                display_message(self.aid.localname, "Через 30 мин вам все доставят")
                message.set_performative(ACLMessage.PROPOSE)
                message.set_content(json.dumps({'bag': self.order}))
                message.add_receiver(AID(name="agent_deliveryman@localhost:8033"))
                self.send(message)


class Deliveryman(Agent):
    def __init__(self, aid):
        super(Deliveryman, self).__init__(aid=aid, debug=False)

    def react(self, message):
        super(Deliveryman, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            bag = content['bag']
            display_message(self.aid.localname, "Я получил сумку {}".format(bag))
            display_message(self.aid.localname, "Я несу сумку")
            display_message(self.aid.localname, "..................")
            display_message(self.aid.localname, "..................")
            display_message(self.aid.localname, "..................")
            display_message(self.aid.localname, "Я принес сумку {}".format(bag))
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'bag': bag, 'name': 'Deliveryman'}))
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            money = content['money']
            display_message(self.aid.localname, "Приятного апптетита!{}".format(money))
            display_message(self.aid.localname, "Приятного апптетита!")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'money': money, 'name': 'Deliveryman'}))
            message.add_receiver(AID(name="agent_pizzeria@localhost:8022"))
            self.send(message)

if __name__ == '__main__':
    agents = list()

    agent_name = 'agent_client@localhost:8011'
    agent_client = Client(AID(name=agent_name))
    agent_pizzeria = Pizzeria(AID(name="agent_pizzeria@localhost:8022"))
    agent_deliveryman = Deliveryman(AID(name='agent_deliveryman@localhost:8033'))

    agents.append(agent_client)
    agents.append(agent_pizzeria)
    agents.append(agent_deliveryman)


    start_loop(agents)

#Организация работы пиццерии 
#Есть 3 агента:Пиццерия,клиент,доставщик
#Сначало клент заказывает еду в пиццерии с лимитом цены 1500,далее пиццерия отдает заказ доставщику,он отдает заказа клиенту и забирает деньги,потом доставщик отдает деньги пиццерии
