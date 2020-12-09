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
            display_message(self.aid.localname, "Мне : {}".format(ageRandomCustomer))
            message = ACLMessage()
            
            if ageRandomCustomer <=18:
                
                self.timeNow+=1
                print(self.timeNow)
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
                elif self.timeNow >=6 & self.timeNow <=22 :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проходите")
                    self.AgeControlPos =0
                    message.set_content(json.dumps({'AgeControlPos':0}))

                elif self.timeNow < 22 & self.timeNow<24 :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Отправить родителям")
                    self.AgeControlPos =1
                    message.set_content(json.dumps({'AgeControlPos':1}))
                self.send(message)
                

            elif ageRandomCustomer>18:
                
                self.timeNow+=1
                print(self.timeNow)
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
                elif self.timeNow >=6 & self.timeNow <=22 :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проходите")
                    self.AgeControlPos =0
                    message.set_content(json.dumps({'AgeControlPos':0}))

                elif self.timeNow < 22 & self.timeNow <24 :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="RandomCustomer@localhost:8011"))
                    display_message(self.aid.localname, "Проходите")
                    self.AgeControlPos =0
                    message.set_content(json.dumps({'AgeControlPos':self.AgeControlPos}))
                self.send(message)
               

class RandomCustomer(Agent):
    def __init__(self, aid):
        super(RandomCustomer, self).__init__(aid=aid, debug=False)
        self.ageRandomCustomer = 0

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
# [AgeControl] 09/12/2020 14:34:31.166 --> Отправить родителям
# [RandomCustomer] 09/12/2020 14:34:31.171 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.173 --> Прийду позже
# [AgeControl] 09/12/2020 14:34:31.176 --> Мне : 12
# 2
# [AgeControl] 09/12/2020 14:34:31.183 --> Отправить родителям
# [RandomCustomer] 09/12/2020 14:34:31.187 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.188 --> Прийду позже
# [AgeControl] 09/12/2020 14:34:31.191 --> Мне : 34
# 3
# [AgeControl] 09/12/2020 14:34:31.193 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.196 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.199 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.203 --> Мне : 34
# 4
# [AgeControl] 09/12/2020 14:34:31.204 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.207 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.208 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.210 --> Мне : 25
# 5
# [AgeControl] 09/12/2020 14:34:31.216 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.221 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.222 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.225 --> Мне : 60
# 6
# [AgeControl] 09/12/2020 14:34:31.227 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.230 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.233 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.237 --> Мне : 32
# 7
# [AgeControl] 09/12/2020 14:34:31.238 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.241 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.242 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.245 --> Мне : 37
# 8
# [AgeControl] 09/12/2020 14:34:31.251 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.255 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.256 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.259 --> Мне : 10
# 9
# [AgeControl] 09/12/2020 14:34:31.260 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.269 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.270 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.273 --> Мне : 32
# 10
# [AgeControl] 09/12/2020 14:34:31.274 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.277 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.282 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.296 --> Мне : 30
# 11
# [AgeControl] 09/12/2020 14:34:31.299 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.304 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.305 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.308 --> Мне : 21
# 12
# [AgeControl] 09/12/2020 14:34:31.310 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.313 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.316 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.320 --> Мне : 65
# 13
# [AgeControl] 09/12/2020 14:34:31.321 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.325 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.325 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.328 --> Мне : 29
# 14
# [AgeControl] 09/12/2020 14:34:31.333 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.337 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.338 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.341 --> Мне : 7
# 15
# [AgeControl] 09/12/2020 14:34:31.343 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.346 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.351 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.354 --> Мне : 16
# 16
# [AgeControl] 09/12/2020 14:34:31.355 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.358 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.359 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.363 --> Мне : 44
# 17
# [AgeControl] 09/12/2020 14:34:31.367 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.370 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.371 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.374 --> Мне : 21
# 18
# [AgeControl] 09/12/2020 14:34:31.375 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.379 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.383 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.387 --> Мне : 65
# 19
# [AgeControl] 09/12/2020 14:34:31.388 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.391 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.392 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.395 --> Мне : 27
# 20
# [AgeControl] 09/12/2020 14:34:31.400 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.404 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.405 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.408 --> Мне : 23
# 21
# [AgeControl] 09/12/2020 14:34:31.409 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.412 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.416 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.419 --> Мне : 17
# 22
# [AgeControl] 09/12/2020 14:34:31.421 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.425 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.426 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.430 --> Мне : 14
# 23
# [AgeControl] 09/12/2020 14:34:31.434 --> Проходите
# [RandomCustomer] 09/12/2020 14:34:31.437 --> Sending Value
# [RandomCustomer] 09/12/2020 14:34:31.438 --> Захожу
# [AgeControl] 09/12/2020 14:34:31.442 --> Мне : 47
# 24
# [AgeControl] 09/12/2020 14:34:31.443 --> Смена закончена
