import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random

class TransportCompanyAgent(Agent):
    def __init__(self, aid):
        super(TransportCompanyAgent, self).__init__(aid=aid, debug=False)  
        self.TransportCompanyAgentPos=1 
        

    def react(self, message):
        super(TransportCompanyAgent, self).react(message)
        if message.performative == ACLMessage.PROPOSE:


            content = json.loads(message.content)
            priceClient = int(content['priceClient'])
            display_message(self.aid.localname, "Хочу отправить посылку по цене : {}".format(priceClient))
            message = ACLMessage()

       
	
                if priceClient == 5000:
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.add_receiver(AID(name="ClientAgent@localhost:8011"))               
                    display_message(self.aid.localname, "Отвезу")
					self.TransportCompanyAgentPos =0
                    message.set_content(json.dumps({'TransportCompanyAgentPos':0}))
		
                elif priceClient >= 3000 & priceClient <4000:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="ClientAgent@localhost:8011"))
                    display_message(self.aid.localname, "Может повысим цену?")
                    self.TransportCompanyAgentPos = 1
                    message.set_content(json.dumps({'TransportCompanyAgentPos':1}))
		
                elif priceClient == 4000 :
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="ClientAgent@localhost:8011"))
                    display_message(self.aid.localname, "Отвезу")
                    self.TransportCompanyAgentPos =0
                    message.set_content(json.dumps({'TransportCompanyAgentPos':0}))

                self.send(message)

               
                if priceClient == 6000:
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.add_receiver(AID(name="ClientAgent@localhost:8011"))               
                    display_message(self.aid.localname, "Отвезу")
					self.TransportCompanyAgentPos =1
                    message.set_content(json.dumps({'TransportCompanyAgentPos':1}))
                elif priceClient >= 5000 & priceClient <= 7000:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="ClientAgent@localhost:8011"))
                    display_message(self.aid.localname, "Так и быть, отвезу")
                    self.TransportCompanyAgentPos =0
                    message.set_content(json.dumps({'TransportCompanyAgentPos':0}))
                
                self.send(message)


class ClientAgent(Agent):
    def __init__(self, aid):
        super(ClientAgent, self).__init__(aid=aid, debug=False)
        self.priceClient = 0

    def on_start(self):
        super().on_start()
        self.call_later(10, self.sendValue)

    def sendValue(self):
        display_message(self.aid.localname, "Sending Value")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'priceClient': self.priceClient}))
        message.add_receiver(AID(name="TransportCompanyAgent@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(ClientAgent, self).react(message)

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            TransportCompanyAgentPos = int(content['TransportCompanyAgentPos'])
	    self.priceClient = =random.randint(3000,7000)
            self.sendValue()
            if TransportCompanyAgentPos == 1:
                display_message(self.aid.localname, "Подумаю")
            elif TransportCompanyAgentPos == 0:
                display_message(self.aid.localname, "Согласен")


if __name__ == '__main__':

    agents = list()


    clientAgent = ClientAgent(AID(name="ClientAgent@localhost:8011"))
    transportCompanyAgent = TransportCompanyAgent(AID(name="TransportCompanyAgent@localhost:8022"))

    agents.append(clientAgent)
    agents.append(transportCompanyAgent)

    start_loop(agents)
	
# [ClientAgent] 18/12/2020 14:34:31.171 --> Sending Value
# [ClientAgent] 18/12/2020 14:34:31.173 --> Хочу отправить посылку по цене : 5000	
# [TransportCompanyAgent] 18/12/2020 14:34:31.166 --> Отвезу
# [ClientAgent] 18/12/2020 14:34:31.171 --> Согласен

# [ClientAgent] 18/12/2020 14:34:31.171 --> Sending Value
# [ClientAgent] 18/12/2020 14:34:31.173 --> Хочу отправить посылку по цене : 3000	
# [TransportCompanyAgent] 18/12/2020 14:34:31.166 --> Может повысим цену?
# [ClientAgent] 18/12/2020 14:34:31.171 --> Подумаю

# [ClientAgent] 18/12/2020 14:34:31.171 --> Sending Value
# [ClientAgent] 18/12/2020 14:34:31.173 --> Хочу отправить посылку по цене : 4000	
# [TransportCompanyAgent] 18/12/2020 14:34:31.166 --> Отвезу
# [ClientAgent] 18/12/2020 14:34:31.171 --> Согласен

# [ClientAgent] 18/12/2020 14:34:31.171 --> Sending Value
# [ClientAgent] 18/12/2020 14:34:31.173 --> Хочу отправить посылку по цене : 6000	
# [TransportCompanyAgent] 18/12/2020 14:34:31.166 --> Отвезу
# [ClientAgent] 18/12/2020 14:34:31.171 --> Подумаю

# [ClientAgent] 18/12/2020 14:34:31.171 --> Sending Value
# [ClientAgent] 18/12/2020 14:34:31.173 --> Хочу отправить посылку по цене : 4000	
# [TransportCompanyAgent] 18/12/2020 14:34:31.166 --> Так и быть, отвезу
# [ClientAgent] 18/12/2020 14:34:31.171 --> Согласен
