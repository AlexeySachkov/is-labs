import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

#единицы измерения тыс руб.
#Покупатель приходит в автосалон, чтобы приобрести автомобиль.Сумма на руках генерируется. Сумма за автомобииль также генерируется.Есть 4 модели, которые отличаются ценовой категорией. Покупатель говорит прдавцу, какую маштну он хочет, и какой суммой располагает. Продавец озвучивает сумму за автомобиль. Если у покупателя сумма достаточная, он покупает.
#Если денег не хватает на покупку, то 2 варианта. Когда у клиента хватает денег на базовую комплектацию (min цена автомобиля), автосалон идет на уступки и снижает цену на автомобиль. Если же суммы не хватает и на базовую комплектацию, то автосалон отказывается снизить стоимость.
class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.price = int(random.randint(500, 900))
        self.model_auto = ['Kia_Rio', 'Kia_Rio_X-Line', 'Kia_Ceed', 'Kia_ProCeed']

    def react(self, message):
        super(Client, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Добрый день!")
            display_message(self.aid.localname, "Я хочу купить машину")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="agent_auto@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            if not flag :
                random_number = int(random.randint(0, 3))
                random_type = self.model_auto[random_number]
                display_message(self.aid.localname, "Я хочу приобрести {} машину".format(random_type))
                display_message(self.aid.localname, "Я располагаю суммой {}".format(self.price))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'price': 0}))
                message.add_receiver(AID(name="agent_auto@localhost:8022"))
                self.send(message)
            else:
                price = content['price']
                if self.price >= price:
                    display_message(self.aid.localname, "Этот вариант мне походит ")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'price': price}))
                    message.add_receiver(AID(name="agent_auto@localhost:8022"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "У меня столько нет")
                    display_message(self.aid.localname, "Сейчас у меня{}".format(self.price))
                    message = ACLMessage()
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'price': self.price}))
                    message.add_receiver(AID(name="agent_auto@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Спасибо, до свидания")



class Auto(Agent):
    def __init__(self, aid):
        super(Auto, self).__init__(aid=aid, debug=False)
        self.model_auto = ['Kia_Rio', 'Kia_Rio_X-Line', 'Kia_Ceed', 'Kia_ProCeed']
        self.type = ''

    def calculate_price(self):
        if self.type == "Kia_Rio":
            return int(random.randint(500, 600))
        elif self.type == "Kia_Rio_X-Line":
            return int(random.randint(600, 700))
        elif self.type == "Kia_Ceed":
            return int(random.randint(700, 800))
        elif self.type == "Kia_ProCeed":
            return int(random.randint(800, 900))

    def min_price(self):
        if self.type == "Kia_Rio":
            return 500
        elif self.type == "Kia_Rio_X-Line":
            return 600
        elif self.type == "Kia_Ceed":
            return 700
        elif self.type == "Kia_ProCeed":
            return 800

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Здравствуйте, вам чем-то помочь?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_client@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Auto, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Да, какую машину выбрали?")
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
                display_message(self.aid.localname, "Она стоит {}".format(price))
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Автосалон получил {}".format(price))
                display_message(self.aid.localname, "Вот ключи от вашей машины")
                display_message(self.aid.localname, "Не забудьте пристегнуть ремни во время поездки")
                display_message(self.aid.localname, "Всего хорошего и до свидания")

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            min_price = self.min_price()
            if min_price <= price:
                display_message(self.aid.localname, "Если вас эта стоимость не устраивает, мы можем снизить стоимость автомобиля")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'flag': True, 'price': price}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Извините, но на этот автомобиль нельзя снизить цену")
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
