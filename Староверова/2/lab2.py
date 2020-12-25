#Имеются весы с чашами, которые необходимо уравнять.

#Есть два аганта:
#1) Scale - первая чаша весов, она статична. Вес на ней выбирается рандомно.
#   Контролирует вес подбираемый на второй чаше.
#2) Person - вторая чаша, человек подбирает вес для уравнения весов.
#   Подбирает вес путем прибавления и убавления значений.

#   Пример: если заданный агентом Scale вес 15, изначальный вес поставленный агентом Person 4,
#           то агент Scale сообщает что выбранный вес меньше нужного и агент Person к своему уже поставленному
#           весу(4) прибавляет еще некоторое число(20). Если добавив это число получится вес(24) больше
#           заданного(15), то агент Scale выдаст сообщение, что получился вес больше нужного. И тогда агент
#           Person будет от своего веса(24) убавлять некоторое число. Так будет продолжаться пока два веса
#           (заданный и подобранный) не будут одинаковы.


import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random
a=random.randint(0,100)
class Scale(Agent):
    def __init__(self, aid):
        super(Scale, self).__init__(aid=aid, debug=False)
        self.unknownWeight = a     
        display_message(self.aid.localname,f"Неизвестный вес {self.unknownWeight}")
        self.scalePos=1
        
    def react(self, message):
        super(Scale, self).react(message)
               
        if message.performative == ACLMessage.PROPOSE:
            
            content = json.loads(message.content)
            weightPerson = int(content['weightPerson'])
            display_message(self.aid.localname, "Got Value: {}".format(weightPerson))
            message = ACLMessage()
            if weightPerson > self.unknownWeight:
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="Person@localhost:8011"))
                self.scalePos =1
                message.set_content(json.dumps({'scalePos':self.scalePos}))
                display_message(self.aid.localname, "Больше нужного веса")
            elif weightPerson == self.unknownWeight:
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="Person@localhost:8011"))
                display_message(self.aid.localname, "Весы уравнены")
            elif weightPerson < self.unknownWeight :
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="Person@localhost:8011"))
                display_message(self.aid.localname, "Меньше нужного веса")
                self.scalePos =0
                message.set_content(json.dumps({'scalePos':0}))
            
            self.send(message)
            
class Person(Agent):
    def __init__(self, aid):
        super(Person, self).__init__(aid=aid, debug=False)
        #self.counter = 0
        self.weightPerson = 0

    def on_start(self):
        super().on_start()
        self.call_later(10, self.sendValue)
        
    def sendValue(self):
        display_message(self.aid.localname, "Sending Value")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'weightPerson': self.weightPerson}))
        message.add_receiver(AID(name="Scale@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(Person, self).react(message)
         
        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            scalePos = int(content['scalePos'])
            step = 10
            b1=random.randint(1,step)
            b2=random.randint(1,b1)
            
            if scalePos == 0 :
                if b1>b2:
                    b1 = b2                
                self.weightPerson = self.weightPerson + b1
                display_message(self.aid.localname,b1)
                self.sendValue()
            elif scalePos == 1:
                self.weightPerson = self.weightPerson - b2
                display_message(self.aid.localname,b2)
                self.sendValue()

if __name__ == '__main__':

    agents = list()

    
    person = Person(AID(name="Person@localhost:8011"))
    scale = Scale(AID(name="Scale@localhost:8022"))

    agents.append(person)
    agents.append(scale)

    start_loop(agents)

    
    
#[Scale] 18/12/2020 18:12:16.951 --> Неизвестный вес 29
#[ams@localhost:8000] 18/12/2020 18:12:16.982 --> Agent Person@localhost:8011 successfully identified.
#[ams@localhost:8000] 18/12/2020 18:12:16.982 --> Agent Scale@localhost:8022 successfully identified.
#[Person@localhost:8011] 18/12/2020 18:12:16.998 --> Identification process done.
#[Scale@localhost:8022] 18/12/2020 18:12:16.998 --> Identification process done.
#[Person] 18/12/2020 18:12:26.976 --> Sending Value
#[Scale] 18/12/2020 18:12:26.976 --> Got Value: 0
#[Scale] 18/12/2020 18:12:26.976 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:26.983 --> 8
#[Person] 18/12/2020 18:12:26.983 --> Sending Value
#[Scale] 18/12/2020 18:12:26.983 --> Got Value: 8
#[Scale] 18/12/2020 18:12:26.983 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:26.998 --> 1
#[Person] 18/12/2020 18:12:26.998 --> Sending Value
#[Scale] 18/12/2020 18:12:26.998 --> Got Value: 9
#[Scale] 18/12/2020 18:12:26.998 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.014 --> 2
#[Person] 18/12/2020 18:12:27.014 --> Sending Value
#[Scale] 18/12/2020 18:12:27.014 --> Got Value: 11
#[Scale] 18/12/2020 18:12:27.014 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.030 --> 2
#[Person] 18/12/2020 18:12:27.030 --> Sending Value
#[Scale] 18/12/2020 18:12:27.030 --> Got Value: 13
#[Scale] 18/12/2020 18:12:27.030 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.045 --> 5
#[Person] 18/12/2020 18:12:27.045 --> Sending Value
#[Scale] 18/12/2020 18:12:27.045 --> Got Value: 18
#[Scale] 18/12/2020 18:12:27.045 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.061 --> 1
#[Person] 18/12/2020 18:12:27.061 --> Sending Value
#[Scale] 18/12/2020 18:12:27.061 --> Got Value: 19
#[Scale] 18/12/2020 18:12:27.061 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.077 --> 9
#[Person] 18/12/2020 18:12:27.077 --> Sending Value
#[Scale] 18/12/2020 18:12:27.083 --> Got Value: 28
#[Scale] 18/12/2020 18:12:27.083 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.083 --> 6
#[Person] 18/12/2020 18:12:27.083 --> Sending Value
#[Scale] 18/12/2020 18:12:27.083 --> Got Value: 34
#[Scale] 18/12/2020 18:12:27.099 --> Больше нужного веса
#[Person] 18/12/2020 18:12:27.130 --> 2
#[Person] 18/12/2020 18:12:27.130 --> Sending Value
#[Scale] 18/12/2020 18:12:27.146 --> Got Value: 32
#[Scale] 18/12/2020 18:12:27.146 --> Больше нужного веса
#[Person] 18/12/2020 18:12:27.146 --> 1
#[Person] 18/12/2020 18:12:27.146 --> Sending Value
#[Scale] 18/12/2020 18:12:27.161 --> Got Value: 31
#[Scale] 18/12/2020 18:12:27.161 --> Больше нужного веса
#[Person] 18/12/2020 18:12:27.161 --> 1
#[Person] 18/12/2020 18:12:27.161 --> Sending Value
#[Scale] 18/12/2020 18:12:27.161 --> Got Value: 30
#[Scale] 18/12/2020 18:12:27.177 --> Больше нужного веса
#[Person] 18/12/2020 18:12:27.183 --> 8
#[Person] 18/12/2020 18:12:27.183 --> Sending Value
#[Scale] 18/12/2020 18:12:27.183 --> Got Value: 22
#[Scale] 18/12/2020 18:12:27.183 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.183 --> 3
#[Person] 18/12/2020 18:12:27.183 --> Sending Value
#[Scale] 18/12/2020 18:12:27.199 --> Got Value: 25
#[Scale] 18/12/2020 18:12:27.199 --> Меньше нужного веса
#[Person] 18/12/2020 18:12:27.199 --> 4
#[Person] 18/12/2020 18:12:27.199 --> Sending Value
#[Scale] 18/12/2020 18:12:27.215 --> Got Value: 29
#[Scale] 18/12/2020 18:12:27.215 --> Весы уравнены
