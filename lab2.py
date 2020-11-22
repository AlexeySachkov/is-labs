import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
import configLab2

class Johny(Agent):
    def __init__(self, aid):
        super(Johny, self).__init__(aid=aid, debug=False)
        random.seed()
        self.Lie =  random.randint(50, 60)
        self.InsightC1 = 0
        self.InsightC2 = 0        
    def react(self, message):
        super(Johny, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            self.InsightC1 = int(content['InsightC1'])
            display_message(self.aid.localname, "~Мой уровень лжи: " + str(self.Lie) + "~")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'InsightC1': self.InsightC1, 'Lie': self.Lie}))
            message.add_receiver(AID(name="mark_civil2@localhost:8033"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            self.InsightC2 = int(content['InsightC2'])
            if self.Lie > self.InsightC1:
                display_message(self.aid.localname, "Thanks Mark. I am so glad to have you as my best friend! Lisa is mafia!")
                configLab2.LP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="mark_civil2@localhost:8033"))
                self.send(message)
            elif self.Lie > self.InsightC2:
                display_message(self.aid.localname, "Oh, what a story Mark! You are mafia!")
                configLab2.MP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="mark_civil2@localhost:8033"))
                self.send(message)
            else:
                display_message(self.aid.localname, random.choice(["You're tearing me apart Lisa! I am not Mafia, you Mafia!", "Everybody betrayed me! I fed up with this world! Lisa, you are mafia!", "I did not hit her, it's not true, I did not hit her. I did not. Oh hi Mark. Lisa is Mafia!"]))
                configLab2.LP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="mark_civil2@localhost:8033"))
                self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            if configLab2.LP == 1:
                display_message(self.aid.localname, "I’m so happy I have Mark as my best friend, lets kill this traitor!")
                configLab2.LP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="lisa_civil1@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Why, Lisa, why, WHYYYYYY?!")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="lisa_civil1@localhost:8011"))
                self.send(message)

class Lisa(Agent):
    def __init__(self, aid):
        super(Lisa, self).__init__(aid=aid, debug=False)
        random.seed()
        self.Insight1 = random.randint(40, 65)
        self.ConvictionC1 = random.randint(40, 60)
        self.Lie = 0
        self.InsightC2 = 0

    def on_start(self):
        super().on_start()
        self.call_later(10, self.first_proposal)

    def first_proposal(self):
        display_message(self.aid.localname, "~Моя проницательность: " + str(self.Insight1) + "~")
        display_message(self.aid.localname, "~Моё убеждение: " + str(self.ConvictionC1) + "~")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'InsightC1': self.Insight1}))
        message.add_receiver(AID(name="johny_mafia@localhost:8022"))
        self.send(message)
        
    def react(self, message):
        super(Lisa, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            self.InsightC2 = int(content['InsightC2'])
            self.Lie = int(content['Lie'])
            if self.Insight1 < self.Lie:
                display_message(self.aid.localname, "I think, Mark is Mafia!")
                configLab2.MP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'InsightC2': self.InsightC2}))
                message.add_receiver(AID(name="johny_mafia@localhost:8022"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Johny, you are disgusting! You are mafia!")
                configLab2.JP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'InsightC2': self.InsightC2}))
                message.add_receiver(AID(name="johny_mafia@localhost:8022"))
                self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            if configLab2.LP == configLab2.JP and configLab2.LP == configLab2.MP:
                display_message(self.aid.localname, "Mark, lets talk, I am not a Mafia. Trust me!")
                configLab2.LP = 0
                configLab2.JP = 0
                configLab2.MP = 0
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.set_content(json.dumps({'ConvictionC1': self.ConvictionC1}))
                message.add_receiver(AID(name="mark_civil2@localhost:8033"))
                self.send(message)
            elif configLab2.MP == 2:
                display_message(self.aid.localname, "So, we kill Mark, but he is not Mafia! We lost...")
                pass
            elif configLab2.JP == 2:
                display_message(self.aid.localname, "We kill Johny and he is a Mafia. Congratulation, Mark!")
                pass
            elif configLab2.LP == 2:
                display_message(self.aid.localname, "You kill me...But... I wasn't a mafia... Live in disgusting world you made...")
                pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Ok, Mark. Let's kill this maniac!")
            configLab2.JP +=1
            message = ACLMessage()
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name="johny_mafia@localhost:8022"))
            self.send(message)
     
class Mark(Agent):
    def __init__(self, aid):
        super(Mark, self).__init__(aid=aid, debug=False)
        random.seed()
        self.InsightC2 = random.randint(30, 70)
        self.ConvictionC2 = random.randint(45, 67)
        self.Lie = 0
        self.InsightC1 = 0

    def react(self, message):
        super(Mark, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            self.InsightC1 = int(content['InsightC1'])
            self.Lie = int(content['Lie'])
            display_message(self.aid.localname, "~Моя проницательность: " + str(self.InsightC2) + "~")
            display_message(self.aid.localname, "~Моё убеждение: " + str(self.ConvictionC2) + "~")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'InsightC2': self.InsightC2, 'Lie': self.Lie}))
            message.add_receiver(AID(name="lisa_civil1@localhost:8011"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            if self.InsightC2 < self.Lie:
                display_message(self.aid.localname, "Hmm, seems like Lisa is Mafia!")
                configLab2.LP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="lisa_civil1@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Holly Molly, Johny is Mafia! KILL THEM ALL.")
                configLab2.JP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="lisa_civil1@localhost:8011"))
                self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            self.ConvictionC1 = int(content['ConvictionC1'])
            if self.ConvictionC1 > self.ConvictionC2:
                display_message(self.aid.localname, "Ok, Lisa. I belive you. So, now I vote for Johny")
                configLab2.JP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="lisa_civil1@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "No, Lisa. You are mafia. Me and Johny will crush you!")
                configLab2.LP +=1
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="johny_mafia@localhost:8011"))
                self.send(message)


if __name__ == '__main__':
    
    
    agents = list()

    civil1 = Lisa(AID(name='lisa_civil1@localhost:8011'))
    mafia = Johny(AID(name='johny_mafia@localhost:8022'))
    civil2 = Mark(AID(name="mark_civil2@localhost:8033"))
    

    agents.append(civil1)
    agents.append(civil2)
    agents.append(mafia)


    start_loop(agents)