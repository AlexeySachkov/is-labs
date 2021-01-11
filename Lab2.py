import json
import random

from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

cAddr = 'client@localhost:59001'
sAddr = 'seller@localhost:59002'

options = ["Dante", "MADI", "SoundGrid", "AES", "AVB"]


class Client(Agent):
    def __init__(self, aid):

        self.budget = random.randint(2000, 15000)
        self.neededOptions = options[int(random.randint(0, 4))]
        self.neededOptionsCnt = random.randint(0, 3)
        self.neededChnl = random.randint(16, 150)
        super(Client, self).__init__(aid=aid, debug=False)

    def on_start(self):
        super().on_start()
        self.outs("Postponed start")
        self.call_later(8, self.callToSeller)

    def sendMsg(self, performative, content):
        message = ACLMessage()
        message.add_receiver(AID(name=sAddr))
        message.set_content(content)
        message.set_performative(performative)
        self.send(message)

    def callToSeller(self):
        self.outs("В бюджете имеется " + str(self.budget))
        self.outs("Звоним диллеру")
        self.sendMsg(ACLMessage.PROPOSE, json.dumps({}))

    def outs(self, msg):
        display_message(self.aid.localname, msg)

    def react(self, message):
        super(Client, self).react(message)

        if (message.performative == ACLMessage.PROPOSE) & (message.sender.name.split('@')[0] == "seller"):
            self.outs("Добрый день. Помогите, пожалуйста, подобрать консоль.")
            self.outs("Мне необходимо примерно " + str(self.neededChnl) + " каналов.")
            msg = json.dumps({'channels': self.neededChnl})
            self.sendMsg(ACLMessage.CONFIRM, msg)

        elif (message.performative == ACLMessage.ACCEPT_PROPOSAL) & (message.sender.name.split('@')[0] == "seller"):
            content = json.loads(message.content)

            if 'neededOptions' in content:
                if (content['neededOptions']) & (self.neededOptionsCnt > 0):
                    self.outs("Да, мне так же необходимы карты расширения типа " + self.neededOptions + " в колличестве " + str(self.neededOptionsCnt))
                    self.outs("Сколько это будет стоить?")
                    msg = json.dumps({'neededOptions': self.neededOptions, 'neededOptionsCnt': self.neededOptionsCnt})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
                else:
                    self.outs("Нет, мне не нужны дополнительные опции")
                    msg = json.dumps({'neededOptionsCnt': self.neededOptionsCnt})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)

            elif 'gotPrice' in content:
                if (content['gotPrice']) & (content['price'] > self.budget):
                    self.outs("Дороговато. Сделаете скидку в " + str((content['price'] - self.budget)) + "?")
                    msg = json.dumps({'discount': True, 'discountAmount': (content['price'] - self.budget)})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
                else:
                    self.outs("То что нужно! Тогда давайте оформим заказ.")
                    msg = json.dumps({'accept': True})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)

            elif 'gotDiscount' in content:
                if content['gotDiscount']:
                    self.outs("Тогда давайте оформим заказ.")
                    msg = json.dumps({'accept': True})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
                else:
                    self.outs("К сожалению такой вариант меня не устраивает. Досвидания.")
                    self.sendMsg(ACLMessage.REJECT_PROPOSAL, {})

        elif (message.performative == ACLMessage.REJECT_PROPOSAL) & (message.sender.name.split('@')[0] == "seller"):
            self.outs("Понятно. Досвидания.")
            self.sendMsg(ACLMessage.REJECT_PROPOSAL, {})


class Seller(Agent):
    def __init__(self, aid):
        super(Seller, self).__init__(aid = aid, debug = False)

        self.deal = []

        self.fin = {}
        self.range = [
            {
                'channels': 16,
                'options': 1,
                'price': 2500
            }, {
                'channels': 48,
                'options': 2,
                'price': 4200
            }, {
                'channels': 64,
                'options': 1,
                'price': 8500
            }, {
                'channels': 128,
                'options': 3,
                'price': 13500
            }]

    def sendMsg(self, performative, content):
        message = ACLMessage()

        message.add_receiver(AID(name=cAddr))
        message.set_content(content)
        message.set_performative(performative)
        self.send(message)

    def outs(self, msg):
        display_message(self.aid.localname, msg)

    def react(self, message):
        super(Seller, self).react(message)

        if (message.performative == ACLMessage.PROPOSE) & (message.sender.name.split('@')[0] == "client"):
            self.outs("Здравствуйте.")
            self.sendMsg(ACLMessage.PROPOSE, json.dumps({}))

        elif (message.performative == ACLMessage.CONFIRM) & (message.sender.name.split('@')[0] == "client"):
            content = json.loads(message.content)
            self.outs("Сейчас посмотрим.")

            flagD = False
            for variant in self.range:
                if variant['channels'] >= content['channels']:
                    flagD = True
                    self.deal.append(variant)

            if (flagD):
                self.outs("У нас есть подходящие варианты. Нужны ли вам дополнительные опции?")
                msg = json.dumps({'neededOptions': True})
                self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
            else:
                self.outs("К сожалению у нас нет подходящей модели. Извините.")
                self.sendMsg(ACLMessage.REJECT_PROPOSAL, {})

        elif (message.performative == ACLMessage.ACCEPT_PROPOSAL) & (message.sender.name.split('@')[0] == "client"):
            content = json.loads(message.content)

            if 'neededOptionsCnt' in content:
                if content['neededOptionsCnt'] > 0:

                    flagO = False
                    for variant in self.deal:
                        if variant['options'] >= content['neededOptionsCnt']:
                            flagO = True
                            self.fin = variant
                            break

                    if flagO:
                        self.outs("Да, есть такая модель")
                        self.outs("Её цена составит " + str(self.fin['price']))
                        msg = json.dumps({'gotPrice': True, 'price': self.fin['price']})
                        self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
                    else:
                        self.outs("К сожалению у нас нет подходящей модели. Извините.")
                        self.sendMsg(ACLMessage.REJECT_PROPOSAL, {})

                else:
                    self.fin = self.deal[0]
                    self.outs("Хорошо. Цена составит " + str(self.fin['price']))
                    msg = json.dumps({'gotPrice': True, 'price': self.fin['price']})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
            elif 'discount' in content:
                if (content['discount']) & (content['discountAmount'] > (self.fin['price'] * 0.15)):
                    self.outs("Мы не можем сделать такую скидку. Извините.")
                    self.sendMsg(ACLMessage.REJECT_PROPOSAL, {})
                else:
                    self.outs("Хорошо, мы можем сделать такую скидку.")
                    msg = json.dumps({'gotDiscount': True})
                    self.sendMsg(ACLMessage.ACCEPT_PROPOSAL, msg)
            elif 'accept' in content:
                if content['accept']:
                    self.outs("Да, давайте. Сейчас отправлю необходимые документы.")

if __name__ == '__main__':
   agents = list()
   client = Client(AID(name=cAddr))
   agents.append(client)
   seller = Seller(AID(name=sAddr))
   agents.append(seller)

   start_loop(agents)