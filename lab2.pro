#Агент Customer - человек, ищущий какой автомобиль себе купить. Знает только что он хочет от автомобиля.
#Агент Consultant - консультант, знает автомобили и их особенности.
#Consultant опрашивает Customer о том, что он хочет от автомобиля. Когда под названные признаки подходит только одна модель автомобиля, называет её
import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv

import random

class Consultant(Agent):
    def __init__(self, aid):
        super(Consultant, self).__init__(aid=aid, debug=False)
        self.known_cars = [["SKODA SUPERB SPORTLINE","Ездить с семьей","Ездить по бездорожью","Коробка автомат"],["LADA 4x4 Vision Concept","Ездить с семьей","Ездить по бездорожью","Возить груз"]]
        self.known_expectations = [];

    def on_start(self):
        super().on_start()

    def ask_for_info(self):
        display_message(self.aid.localname, "Что вы хотите от автомобиля?" if len(self.known_expectations) == 0 else "А что еще?")
        message = ACLMessage()
        message.set_performative(ACLMessage.NOT_UNDERSTOOD)
        message.add_receiver(AID(name="Customer@localhost:8022"))
        self.send(message)
        
    def send_conclusion(self,idx):
        display_message(self.aid.localname, "Вам пойдет {}".format(self.known_cars[idx][0]))
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'car': self.known_cars[idx][0]}))
        message.add_receiver(AID(name="Customer@localhost:8022"))
        self.send(message)
        
    def send_refuse(self):
        display_message(self.aid.localname, "Таких машин у нас в каталоге нет...")
        message = ACLMessage()
        message.set_performative(ACLMessage.REFUSE)
        message.add_receiver(AID(name="Customer@localhost:8022"))
        self.send(message)
        
    def try_to_conclude(self):
        occurences = []
        for i in range(len(self.known_expectations)):
            occurences.append([])
            for j in range(len(self.known_cars)):
                for k in range(len(self.known_cars[j])):
                    if(self.known_cars[j][k] == self.known_expectations[i]):
                        occurences[i].append(j)
        if(len(occurences) == 1 and len(occurences[0]) != 1):
            self.ask_for_info()
            return
        elif(len(occurences) == 1 and len(occurences[0]) == 1):
            self.send_conclusion(occurences[0][0])
            return
        list1 = occurences[0]
        for i in range(len(occurences)-1):
            list1 = list(set(list1).intersection(occurences[i+1]))
        if(len(list1) > 1):
            self.ask_for_info()
            return
        elif(len(list1) < 1):
            self.send_refuse()
        else:
            self.send_conclusion(list1[0])
            return

    def react(self, message):
        super(Consultant, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Сейчас посмотрим.")
            self.ask_for_info()
        elif message.performative == ACLMessage.QUERY_REF:
            content = json.loads(message.content)
            if(content['observation'] != 0):
                observation = str(content['observation'])
                self.known_expectations.append(observation)
                self.try_to_conclude()
            else:
                self.send_refuse()

class Customer(Agent):
    def __init__(self, aid):
        super(Customer, self).__init__(aid=aid, debug=False)
        self.expectations = ["Ездить с семьей","Ездить по бездорожью","Возить груз"]
        self.timesAsked = 0;

    def on_start(self):
        super().on_start()
        self.call_later(10, self.ask_for_help)
        
    def ask_for_help(self):
        display_message(self.aid.localname, "Помогите мне выбрать, какой автомобиль мне купить.")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="Consultant@localhost:8011"))
        self.send(message)
        
    def send_info(self):
        observation = self.expectations[self.timesAsked]
        self.timesAsked = self.timesAsked + 1
        display_message(self.aid.localname, "{} - вот, что я жду от автомобиля.".format(observation))
        message = ACLMessage()
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'observation': observation}))
        message.add_receiver(AID(name="Consultant@localhost:8011"))
        self.send(message)
    
    def send_no_more(self):
        display_message(self.aid.localname, "Я перечислил всё, что хотел.")
        message = ACLMessage()
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'observation': 0}))
        message.add_receiver(AID(name="Consultant@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Customer, self).react(message)
        if message.performative == ACLMessage.NOT_UNDERSTOOD:
            if(self.timesAsked < len(self.expectations)):
                self.send_info()
            else:
                self.send_no_more()
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            car = str(content['car'])
            display_message(self.aid.localname, "{}, понял. Спасибо.".format(car))
        if message.performative == ACLMessage.REFUSE:
            display_message(self.aid.localname, "Эх... Неужели я хочу слишком многого?")



if __name__ == '__main__':

    agents = list()

    consultant = Consultant(AID(name='Consultant@localhost:8011'))
    customer = Customer(AID(name='Customer@localhost:8022'))

    agents.append(consultant)
    agents.append(customer)

    start_loop(agents)
