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
