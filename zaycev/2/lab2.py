#Работа книжного магазина
#Агент Seller -продавец, имеет базу книг и базу цен.
#Агент Customer - покупатель, ищет книгу.
#Seller спрашивает у Customer автора и название книги,после чего выдает ее цену.Customer может согласиться или отказаться ее покупать.

import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random

books = [["L.N. Tolstoy","War and Peace"],["L.N. Tolstoy","Anna Karenina"],["L.N. Tolstoy","Resurrection"],
	["S.E. King","Carrie"],["S.E. King","Firestarter"],["S.E. King","Black House"]]

costs = [[100],[200],[150],[50],[300],[100]]

class Customer(Agent):
    def __init__(self, aid):
        super(Customer, self).__init__(aid=aid, debug=False)
        self.get_knowledge()
        self.timesAsked = 0;

    def get_knowledge(self):
        num = random.randint(0,len(books)-1)
        self.knowledge = books[num][0:len(books[num])]
        self.knowledge2 = costs[num][0]

    def on_start(self):
        super().on_start()
        self.call_later(10, self.ask_for_help)

    def ask_for_help(self):
        display_message(self.aid.localname, "I'm looking for a book, please help me.")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="seller@localhost:8011"))
        self.send(message)

    def send_info(self):
        knowledge = self.knowledge[self.timesAsked]
        self.timesAsked = self.timesAsked + 1
        display_message(self.aid.localname, "{}.".format(knowledge))
        message = ACLMessage()
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'knowledge': knowledge}))
        message.add_receiver(AID(name="seller@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Customer, self).react(message)
        if message.performative == ACLMessage.NOT_UNDERSTOOD:
            self.send_info()
        if (message.performative == ACLMessage.PROPOSE and self.knowledge2 <= 150):
            display_message(self.aid.localname, "Okay, I'll buy it. Thanks.")
        if (message.performative == ACLMessage.PROPOSE and self.knowledge2 > 150):
            display_message(self.aid.localname, "Thank you for the information, but I can't buy it, thank you.")

class Seller(Agent):
    def __init__(self, aid):
        super(Seller, self).__init__(aid=aid, debug=False)
        self.knownBooks = books
        self.knownCost = costs
        self.knownKnowledges = [];

    def get_knowledge2(self):
        num = random.randint(0,len(books)-1)
        self.knowledge2 = cost[num][0]

    def on_start(self):
        super().on_start()

    def ask_for_info(self):
        display_message(self.aid.localname, "What author are you looking for?" if len(self.knownKnowledges) == 0 else "What is the name of the work?")
        message = ACLMessage()
        message.set_performative(ACLMessage.NOT_UNDERSTOOD)
        message.add_receiver(AID(name="customer@localhost:8022"))
        self.send(message)

    def send_conclusion(self,idx):
        display_message(self.aid.localname, "Yes we have this book by {}.".format(self.knownBooks[idx][0]))
        display_message(self.aid.localname, "It costs {}".format(self.knownCost[idx][0]))
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'costs': self.knownCost[idx][0]}))
        message.add_receiver(AID(name="customer@localhost:8022"))
        self.send(message)

    def compareFacts(self):
        informations = []
        for i in range(len(self.knownKnowledges)):
            informations.append([])
            for j in range(len(self.knownBooks)):
                for k in range(len(self.knownBooks[j])):
                    if(self.knownBooks[j][k] == self.knownKnowledges[i]):
                        informations[i].append(j)
        if(len(informations) == 1 and len(informations[0]) != 1):
            self.ask_for_info()
            return
        elif(len(informations) == 1 and len(informations[0]) == 1):
            self.send_conclusion(informations[0][0])
            return
        list1 = informations[0]
        for i in range(len(informations)-1):
            list1 = list(set(list1).intersection(informations[i+1]))
        if(len(list1) > 1):
            self.ask_for_info()
            return
        elif(len(list1) < 1):
            self.send_refuse()
        else:
            self.send_conclusion(list1[0])
            return

    def react(self, message):
        super(Seller, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Okay.")
            self.ask_for_info()
        elif message.performative == ACLMessage.QUERY_REF:
            content = json.loads(message.content)
            knowledge = str(content['knowledge'])
            self.knownKnowledges.append(knowledge)
            self.compareFacts()

if __name__ == '__main__':

    agents = list()

    seller = Seller(AID(name='seller@localhost:8011'))
    customer = Customer(AID(name='customer@localhost:8022'))

    agents.append(seller)
    agents.append(customer)

    start_loop(agents)

#[customer] 28/11/2020 08:09:03.504 --> I'm looking for a book, please help me.
#[seller] 28/11/2020 08:09:03.510 --> Okay.
#[seller] 28/11/2020 08:09:03.510 --> What author are you looking for?
#[customer] 28/11/2020 08:09:03.518 --> L.N. Tolstoy.
#[seller] 28/11/2020 08:09:03.526 --> What is the name of the work?
#[customer] 28/11/2020 08:09:03.532 --> Resurrection.
#[seller] 28/11/2020 08:09:03.536 --> Yes we have this book by L.N. Tolstoy.
#[seller] 28/11/2020 08:09:03.537 --> It costs 150
#[customer] 28/11/2020 08:09:03.540 --> Okay, I'll buy it. Thanks.
