#Ситуация: человек хочет купить определенные виды трав в травном магазине.
#Клиент хочет купить некоторые виды трав по определенной цене.
#Изначально в магазине меньше трав, чем требует клиент. И магазин наказывает травнику собирать травы.
#Диалог травника и магазина заканчивается, когда травник соберет нужное кол-во трав.
#Потом магазин говорит, что все окей, у нас есть нужно кол-во трав.
#Цена на травы зависит от кол-во трав.
#Если цена на травы высокая, то клиент расстраивается.
#Магазин предлагает подождать, и говорит травнику ещё раз собрать травы. Так как травник собирает травы
#рандомно, то есть шанс собрать необходимое кол-во трав, чтобы цена на них упала. И тогда клиент с радостью
#покупает определенный вид трав. В противном случае, если травник не собрал нужное кол-во трав, чтоб цена
#изменилась, то магазин говорит клиенту, что травы редкие и цену на них снизить не могут. В этом случае клиент
#не покупает данный вид трав. Далее магазин спрашивает, может быть клиент хочет какие-нибудь ещё травы. На
#что клиент идет дальше по списку трав, которые он хочет купить. В конце клиент какие-то травы купил, а какие-
#то слишком дорогие и он их не стал покупать.


import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

class Herbalist(Agent):
    def __init__(self, aid):
        super(Herbalist, self).__init__(aid=aid, debug=False)
        self.bag = {"зверобой": 0, "шалфей": 0, "эвкалипт": 0,
                    "полынь": 0, "бессмертник": 0, "календула": 0,
                    "лен": 0, "ромашка": 0, "чабрец": 0}

    def herbs_finder(self):
        for key in self.bag:
            self.bag[key] += int(random.randint(1, 2)/2) + int(random.randint(1, 4)/4) + int(random.randint(1, 6)/6)

    def clean_bag(self):
        for key in self.bag:
            self.bag[key] = 0

    def react(self, message):
        super(Herbalist, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            self.clean_bag()
            display_message(self.aid.localname, "Поиск трав")
            self.herbs_finder()
            display_message(self.aid.localname, "Вот что я нашёл")
            display_message(self.aid.localname, "{}".format(self.bag))
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            bag = self.bag
            bag['name'] = "Herbalist"
            message.set_content(json.dumps(bag))
            message.add_receiver(AID(name="agent_herbal_shop@localhost:8022"))
            self.send(message)
            bag.pop('name')

class Herbal_shop(Agent):
    def __init__(self, aid):
        super(Herbal_shop, self).__init__(aid=aid, debug=False)
        self.storage = {"зверобой": 5, "шалфей": 5, "эвкалипт": 5,
                        "полынь": 5, "бессмертник": 5, "календула": 5,
                        "лен": 5, "ромашка": 5, "чабрец": 5}
        self.type = ""
        self.number = 0
        self.price = 0
        self.happy = True

    def recalculate_prices(self, key):
        if self.storage[key] <= 10:
            self.price = 100
        elif 10 < self.storage[key] <= 15:
            self.price = 80
        elif 15 < self.storage[key]:
            self.price = 60

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Желаете что-то купить?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_client@localhost:8011"))
        self.send(message)

    def replenishment_storage(self, bag):
        for key in self.storage:
            self.storage[key] = self.storage[key] + bag[key]

    def react(self, message):
        super(Herbal_shop, self).react(message)
        #message = ACLMessage()
        if message.performative == ACLMessage.PROPOSE:
            content1 = json.loads(message.content)
            self.type = content1['type']
            self.number = int(content1['number'])
            self.happy = True
            message = ACLMessage()
            display_message(self.aid.localname, "Магазин получил предложение на {} трав типа: {}".format(self.number, self.type))
            if self.storage[self.type] >= self.number:
                display_message(self.aid.localname, "В магазине есть нужно количество такого вида трав: {}".format(self.type))
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                self.recalculate_prices(self.type)
                display_message(self.aid.localname, "За 1 шт: {}".format(self.price))
                content = {'type': self.type, 'price': self.price}
                message.set_content(json.dumps(content))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "К сожалению, у нас нет столько трав этого вида: {}".format(self.type))
                display_message(self.aid.localname, "Пожалуйста, подождите")
                message.set_performative(ACLMessage.PROPOSE)
                message.add_receiver(AID(name="agent_herbalist@localhost:8033"))
                self.send(message)

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            happy = content['happy']
            bag_full = content['Bag']
            message = ACLMessage()
            if (happy == "True") and (bag_full == "no_full"):
                self.happy = False
                display_message(self.aid.localname, "Подождите, мы посмотрим, что можно сделать")
                message.set_performative(ACLMessage.PROPOSE)
                display_message(self.aid.localname, "Травник принеси, пожалуйста, ещё трав")
                message.add_receiver(AID(name="agent_herbalist@localhost:8033"))
                self.send(message)
            elif (happy == "False") and (bag_full == "no_full"):
                display_message(self.aid.localname, "Желаете что-нибудь ещё?")
                message.set_performative(ACLMessage.PROPOSE)
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            elif (happy == "True") and (bag_full == "full"):
                display_message(self.aid.localname, "Спасибо за покупки!")
                display_message(self.aid.localname, "Удачного дня!")

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            name = content.pop('name')
            bag = content
            message = ACLMessage()
            if name == "Herbalist":
                #display_message(self.aid.localname, "Травник принес в магазин трав: {}".format(bag))
                self.replenishment_storage(bag)
                display_message(self.aid.localname, "Все травы магазина: {}".format(self.storage))
                if self.storage[self.type] <= self.number:
                    display_message(self.aid.localname, "Трав не хвататет, пожалуйста, принеси ещё")
                    message.set_performative(ACLMessage.PROPOSE)
                    message.add_receiver(AID(name="agent_herbalist@localhost:8033"))
                    self.send(message)
                elif not self.happy:
                    price = self.price
                    self.recalculate_prices(self.type)
                    if price == self.price:
                        display_message(self.aid.localname, "Травы очень редкие, мы можем продать только по {}".format(self.price))
                        message.set_performative(ACLMessage.REJECT_PROPOSAL)
                        message.add_receiver(AID(name="agent_client@localhost:8011"))
                        self.send(message)
                    elif price > self.price:
                        display_message(self.aid.localname, "Мы можем продать подешле, только для вас! по {} за шт".format(self.price))
                        message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                        content = {'type': self.type, 'price': self.price}
                        message.set_content(json.dumps(content))
                        message.add_receiver(AID(name="agent_client@localhost:8011"))
                        self.send(message)
                else:
                    display_message(self.aid.localname, "В магазине есть нужно количество такого вида трав: {}".format(self.type))
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    self.recalculate_prices(self.type)
                    display_message(self.aid.localname, "За 1 шт: {}".format(self.price))
                    content = {'type': self.type, 'price': self.price}
                    message.set_content(json.dumps(content))
                    message.add_receiver(AID(name="agent_client@localhost:8011"))
                    self.send(message)
            else:
                display_message(self.aid.localname, "Спасибо за покупку!")
                self.storage[self.type] -= self.number
                display_message(self.aid.localname, "Желаете что-то ещё?")
                message.set_performative(ACLMessage.PROPOSE)
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)


class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.list = ["зверобой", "шалфей", "эвкалипт",
                     "полынь", "бессмертник", "календула",
                     "лен", "ромашка", "чабрец"]

        self.client_bag = {"зверобой": 0, "шалфей": 0, "эвкалипт": 0,
                           "полынь": 0, "бессмертник": 0, "календула": 0,
                           "лен": 0, "ромашка": 0, "чабрец": 0}

        self.counter = 0
        self.price = 70



    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            if self.counter < len(self.list):
                display_message(self.aid.localname, "Хочу купить 10 шт травы вида: {}".format(self.list[self.counter]))
                message = ACLMessage()
                message.set_performative(ACLMessage.PROPOSE)
                content = {'type': self.list[self.counter], 'number': 10}
                message.set_content(json.dumps(content))
                message.add_receiver(AID(name="agent_herbal_shop@localhost:8022"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Спасибо больше ничего не надо")
                display_message(self.aid.localname, "В итоге клиент купил {}".format(self.client_bag))
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                content = {'happy': "True", 'Bag': "full"}
                message.set_content(json.dumps(content))
                message.add_receiver(AID(name="agent_herbal_shop@localhost:8022"))
                self.send(message)

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            type = content['type']
            price = int(content['price'])
            if price >= self.price:
                display_message(self.aid.localname, "Дорого! Может быть продадите дешевле?")
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                content = {'happy': "True", 'Bag': "no_full"}
                message.set_content(json.dumps(content))
                message.add_receiver(AID(name="agent_herbal_shop@localhost:8022"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Отлично! Покупаю 10 шт травы вида: {}".format(type))
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                content = {'type': self.list[self.counter], 'name': "Client"}
                message.set_content(json.dumps(content))
                message.add_receiver(AID(name="agent_herbal_shop@localhost:8022"))
                self.client_bag[self.list[self.counter]] += 10
                self.send(message)
                self.counter += 1

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Печально :(")
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            content = {'happy': "False", 'Bag': "no_full"}
            message.set_content(json.dumps(content))
            message.add_receiver(AID(name="agent_herbal_shop@localhost:8022"))
            self.send(message)
            self.counter += 1





if __name__ == '__main__':
    agents = list()

    agent_name = 'agent_client@localhost:8011'
    agent_client = Client(AID(name=agent_name))
    agent_herbal_shop = Herbal_shop(AID(name="agent_herbal_shop@localhost:8022"))
    agent_herbalist = Herbalist(AID(name='agent_herbalist@localhost:8033'))

    agents.append(agent_client)
    agents.append(agent_herbal_shop)
    agents.append(agent_herbalist)

    start_loop(agents)
