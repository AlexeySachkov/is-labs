# agent_example_1.py
# A simple hello agent in PADE!
import json

from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv

class Agent2(Agent):
    def __init__(self, aid):
        super(Agent2, self).__init__(aid=aid, debug=False)
        self.max_price = 50

    def react(self, message):
        super(Agent2, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            price = int(content['price'])
            display_message(self.aid.localname, "Got proposal: {}".format(price))
            message = ACLMessage()
            if price < self.max_price:
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="agent_hello@localhost:8011"))
                display_message(self.aid.localname, "Accepted")
            else:
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="agent_hello@localhost:8011"))
                display_message(self.aid.localname, "Rejected")
            self.send(message)




class AgenteHelloWorld(Agent):
    def __init__(self, aid):
        super(AgenteHelloWorld, self).__init__(aid=aid, debug=False)
        self.counter = 0
        self.price = 100

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_prosal)

    def send_prosal(self):
        display_message(self.aid.localname, "sending proposal")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'price': self.price}))
        message.add_receiver(AID(name="agent2@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(AgenteHelloWorld, self).react(message)

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            self.price = self.price - 10
            self.send_prosal()



if __name__ == '__main__':

    agents = list()

    agent_name = 'agent_hello@localhost:8011'
    agente_hello = AgenteHelloWorld(AID(name=agent_name))
    agent2 = Agent2(AID(name="agent2@localhost:8022"))

    agents.append(agente_hello)
    agents.append(agent2)

    start_loop(agents)