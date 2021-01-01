# Агент AgrControl получает значения возраста от RandomCustomer и решает на основе возраста и времени 
# пропускать посетителя или нет


import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random

class AgeControl(Agent):
    def __init__(self, aid):
        super(AgeControl, self).__init__(aid=aid, debug=False)  
        self.AgeControlPos=1
        self.timeNow = 0

    def react(self, message):
        super(AgeControl, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            
            
            content = json.loads(message.content)
            ageRandomCustomer = int(content['ageRandomCustomer'])
            
            message = ACLMessage()
            self.timeNow+=1
            print(self.timeNow)
            display_message(self.aid.localname, "Мне : {}".format(ageRandomCustomer))
            if ageRandomCustomer <=18:
                if self.timeNow == 24:
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))               
                    display_message(self.aid.localname, "Смена закончена")
                elif self.timeNow < 6:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Отправить родителям")
                    self.AgeControlPos =1
                    message.set_content(json.dumps({'AgeControlPos':1}))
                elif (self.timeNow >=6) and (self.timeNow <21) :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проходите")
                    self.AgeControlPos =0
                    message.set_content(json.dumps({'AgeControlPos':0}))
                elif (self.timeNow >= 21) and (self.timeNow<24) :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Отправить родителям")
                    self.AgeControlPos =1
                    message.set_content(json.dumps({'AgeControlPos':1}))
                self.send(message)
                

            elif ageRandomCustomer>18:
                if self.timeNow == 24:
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))               
                    display_message(self.aid.localname, "Смена закончена")
                elif self.timeNow < 6:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проходите")
                    self.AgeControlPos =0
                    message.set_content(json.dumps({'AgeControlPos':self.AgeControlPos}))
                elif (self.timeNow >=6) and (self.timeNow <21) :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проход закрыт")
                    self.AgeControlPos =1
                    message.set_content(json.dumps({'AgeControlPos':self.AgeControlPos}))
                elif (self.timeNow >= 21) and (self.timeNow <24) :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проходите")
                    self.AgeControlPos =0
                    message.set_content(json.dumps({'AgeControlPos':self.AgeControlPos}))
                self.send(message)
               

class RandomCustomer(Agent):
    def __init__(self, aid):
        super(RandomCustomer, self).__init__(aid=aid, debug=False)
        self.ageRandomCustomer = random.randint(5,65)

    def on_start(self):
        super().on_start()
        self.call_later(10, self.sendValue)
        
    def sendValue(self):
        display_message(self.aid.localname, "Sending Value")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'ageRandomCustomer': self.ageRandomCustomer}))
        message.add_receiver(AID(name="AgeControl@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(RandomCustomer, self).react(message)
        
        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            AgeControlPos = int(content['AgeControlPos'])
            self.ageRandomCustomer=random.randint(5,65)
            self.sendValue()
            if AgeControlPos == 1:
                display_message(self.aid.localname, "Прийду позже")
            elif AgeControlPos == 0:
                display_message(self.aid.localname, "Захожу")
            

if __name__ == '__main__':

    agents = list()

    
    randomCustomer = RandomCustomer(AID(name="RandomCustomer@localhost:8011"))
    ageControl = AgeControl(AID(name="AgeControl@localhost:8022"))

    agents.append(randomCustomer)
    agents.append(ageControl)

    start_loop(agents)




# 1
# [AgeControl] 31/12/2020 01:40:49.804 --> Мне : 62
# [AgeControl] 31/12/2020 01:40:49.805 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:49.808 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.810 --> Захожу
# 2
# [AgeControl] 31/12/2020 01:40:49.820 --> Мне : 45
# [AgeControl] 31/12/2020 01:40:49.821 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:49.836 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.837 --> Захожу
# 3
# [AgeControl] 31/12/2020 01:40:49.842 --> Мне : 24
# [AgeControl] 31/12/2020 01:40:49.842 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:49.846 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.851 --> Захожу
# 4
# [AgeControl] 31/12/2020 01:40:49.856 --> Мне : 61
# [AgeControl] 31/12/2020 01:40:49.857 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:49.860 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.862 --> Захожу
# 5
# [AgeControl] 31/12/2020 01:40:49.870 --> Мне : 7
# [AgeControl] 31/12/2020 01:40:49.871 --> Отправить родителям
# [RandomCustomer] 31/12/2020 01:40:49.874 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.875 --> Прийду позже
# 6
# [AgeControl] 31/12/2020 01:40:49.878 --> Мне : 64
# [AgeControl] 31/12/2020 01:40:49.878 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.888 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.889 --> Прийду позже
# 7
# [AgeControl] 31/12/2020 01:40:49.892 --> Мне : 28
# [AgeControl] 31/12/2020 01:40:49.893 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.896 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.902 --> Прийду позже
# 8
# [AgeControl] 31/12/2020 01:40:49.918 --> Мне : 44
# [AgeControl] 31/12/2020 01:40:49.920 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.924 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.925 --> Прийду позже
# 9
# [AgeControl] 31/12/2020 01:40:49.928 --> Мне : 49
# [AgeControl] 31/12/2020 01:40:49.929 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.938 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.939 --> Прийду позже
# 10
# [AgeControl] 31/12/2020 01:40:49.943 --> Мне : 21
# [AgeControl] 31/12/2020 01:40:49.944 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.948 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.952 --> Прийду позже
# 11
# [AgeControl] 31/12/2020 01:40:49.956 --> Мне : 63
# [AgeControl] 31/12/2020 01:40:49.957 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.960 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.960 --> Прийду позже
# 12
# [AgeControl] 31/12/2020 01:40:49.968 --> Мне : 25
# [AgeControl] 31/12/2020 01:40:49.970 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.973 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.974 --> Прийду позже
# 13
# [AgeControl] 31/12/2020 01:40:49.977 --> Мне : 41
# [AgeControl] 31/12/2020 01:40:49.978 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:49.981 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:49.986 --> Прийду позже
# 14
# [AgeControl] 31/12/2020 01:40:50.002 --> Мне : 32
# [AgeControl] 31/12/2020 01:40:50.003 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:50.007 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.008 --> Прийду позже
# 15
# [AgeControl] 31/12/2020 01:40:50.011 --> Мне : 25
# [AgeControl] 31/12/2020 01:40:50.011 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:50.015 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.019 --> Прийду позже
# 16
# [AgeControl] 31/12/2020 01:40:50.023 --> Мне : 60
# [AgeControl] 31/12/2020 01:40:50.024 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:50.027 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.028 --> Прийду позже
# 17
# [AgeControl] 31/12/2020 01:40:50.034 --> Мне : 28
# [AgeControl] 31/12/2020 01:40:50.036 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:50.039 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.040 --> Прийду позже
# 18
# [AgeControl] 31/12/2020 01:40:50.043 --> Мне : 22
# [AgeControl] 31/12/2020 01:40:50.044 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:50.047 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.052 --> Прийду позже
# 19
# [AgeControl] 31/12/2020 01:40:50.055 --> Мне : 11
# [AgeControl] 31/12/2020 01:40:50.056 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:50.060 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.060 --> Захожу
# 20
# [AgeControl] 31/12/2020 01:40:50.068 --> Мне : 38
# [AgeControl] 31/12/2020 01:40:50.069 --> Проход закрыт
# [RandomCustomer] 31/12/2020 01:40:50.072 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.073 --> Прийду позже
# 21
# [AgeControl] 31/12/2020 01:40:50.076 --> Мне : 38
# [AgeControl] 31/12/2020 01:40:50.077 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:50.080 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.085 --> Захожу
# 22
# [AgeControl] 31/12/2020 01:40:50.088 --> Мне : 12
# [AgeControl] 31/12/2020 01:40:50.089 --> Отправить родителям
# [RandomCustomer] 31/12/2020 01:40:50.092 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.093 --> Прийду позже
# 23
# [AgeControl] 31/12/2020 01:40:50.101 --> Мне : 55
# [AgeControl] 31/12/2020 01:40:50.102 --> Проходите
# [RandomCustomer] 31/12/2020 01:40:50.105 --> Sending Value
# [RandomCustomer] 31/12/2020 01:40:50.106 --> Захожу
# 24
# [AgeControl] 31/12/2020 01:40:50.120 --> Мне : 52
# [AgeControl] 31/12/2020 01:40:50.122 --> Смена закончена
