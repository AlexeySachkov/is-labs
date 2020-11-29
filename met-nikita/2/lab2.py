#Агент Guided - заблудившийся человек, знает только о том что вокруг него
#Агент Guide - удаленный помощник, названия локаций и их признаки
#Guide опрашивает Guided о признаках места, где он находится, по-одному. Когда под названные признаки подходит только одна локация, называет её
import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random

locations = [["Polevaya st.","Big white building","Medical center","Shop","Memorial"],["Pobedy sqr.","Big white building","Shop","Medical center","Subway station"]]

class Guided(Agent):
    def __init__(self, aid):
        super(Guided, self).__init__(aid=aid, debug=False)
        self.get_observed()
        self.timesAsked = 0;
    
    def get_observed(self):
        num = random.randint(0,len(locations)-1)
        self.observed = locations[num][1:len(locations[num])]

    def on_start(self):
        super().on_start()
        self.call_later(10, self.ask_for_help)
        
    def ask_for_help(self):
        display_message(self.aid.localname, "I'm lost. Please help me understand where I am.")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="guide@localhost:8011"))
        self.send(message)
        
    def send_info(self):
        observation = self.observed[self.timesAsked]
        self.timesAsked = self.timesAsked + 1
        display_message(self.aid.localname, "I see {}.".format(observation))
        message = ACLMessage()
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'observation': observation}))
        message.add_receiver(AID(name="guide@localhost:8011"))
        self.send(message)
    
    def send_no_more(self):
        display_message(self.aid.localname, "I don't see anything else.")
        message = ACLMessage()
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'observation': 0}))
        message.add_receiver(AID(name="guide@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Guided, self).react(message)
        if message.performative == ACLMessage.NOT_UNDERSTOOD:
            if(self.timesAsked < len(self.observed)):
                self.send_info()
            else:
                self.send_no_more()
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            location = str(content['location'])
            display_message(self.aid.localname, "{}, got it. Thanks.".format(location))
        if message.performative == ACLMessage.REFUSE:
            display_message(self.aid.localname, "Damn... Thanks anyway.")




class Guide(Agent):
    def __init__(self, aid):
        super(Guide, self).__init__(aid=aid, debug=False)
        self.knownLocations = locations
        self.knownObservations = [];

    def on_start(self):
        super().on_start()

    def ask_for_info(self):
        display_message(self.aid.localname, "What do you see nearby?" if len(self.knownObservations) == 0 else "What else do you see?")
        message = ACLMessage()
        message.set_performative(ACLMessage.NOT_UNDERSTOOD)
        message.add_receiver(AID(name="guided@localhost:8022"))
        self.send(message)
        
    def send_conclusion(self,idx):
        display_message(self.aid.localname, "You are on {}".format(self.knownLocations[idx][0]))
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'location': self.knownLocations[idx][0]}))
        message.add_receiver(AID(name="guided@localhost:8022"))
        self.send(message)
        
    def send_refuse(self):
        display_message(self.aid.localname, "Can't help, don't know such place...")
        message = ACLMessage()
        message.set_performative(ACLMessage.REFUSE)
        message.add_receiver(AID(name="guided@localhost:8022"))
        self.send(message)
        
    def compareFacts(self):
        occurences = []
        for i in range(len(self.knownObservations)):
            occurences.append([])
            for j in range(len(self.knownLocations)):
                for k in range(len(self.knownLocations[j])):
                    if(self.knownLocations[j][k] == self.knownObservations[i]):
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
        super(Guide, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Okay.")
            self.ask_for_info()
        elif message.performative == ACLMessage.QUERY_REF:
            content = json.loads(message.content)
            if(content != 0):
                observation = str(content['observation'])
                self.knownObservations.append(observation)
                self.compareFacts()
            else:
                self.send_refuse()



if __name__ == '__main__':

    agents = list()

    guide = Guide(AID(name='guide@localhost:8011'))
    guided = Guided(AID(name='guided@localhost:8022'))

    agents.append(guide)
    agents.append(guided)

    start_loop(agents)