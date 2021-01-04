import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

class Worker(Agent):
    def __init__(self, aid):
        super(Worker, self).__init__(aid=aid, debug=False)
        self.salary = int(random.randint(5000, 50000))
        self.experience = int(random.randint(0, 10))
        self.languages = ['PHP', 'C++', 'Java', 'C#']
        self.frameworks = ['.NET', 'JavaFx', 'Yii2', 'Spring']
        self.known_frameworks = []
        self.known_languages = []

    def post(self, performative, content):
        message = ACLMessage()
        message.add_receiver(AID(name="employer@localhost:8022"))
        message.set_content(json.dumps(content))
        message.set_performative(performative)
        self.send(message)

    def print(self, msg):
        display_message(self.aid.localname, msg)

    def intersection(self, list1, list2):
        return list(set(list1) & set(list2))

    def react(self, message):
        super(Worker, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            self.print("Hi, I've heard you're looking for developers!")
            self.post(ACLMessage.PROPOSE, {})

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)

            req_languages = content['languages']
            req_frameworks = content['frameworks']
            offer = content['offer']

            if req_languages:
                self.known_languages = self.intersection(req_languages, self.languages)
                if len(self.known_languages) > 0:
                    self.print('Sure, I`ve been worked with it!')
                    self.print('For a {} years...'.format(self.experience))
                    self.post(ACLMessage.ACCEPT_PROPOSAL, {'known_languages': self.known_languages, 'experience': self.experience, 'known_frameworks': self.known_frameworks})
                else:
                    self.print('Oh, I`m sorry!')
                    self.print(self.known_languages)
                    self.post(ACLMessage.ACCEPT_PROPOSAL, {'known_languages': False, 'experience': False})

            elif req_frameworks:
                self.known_frameworks = self.intersection(req_frameworks, self.frameworks)
                if(len(self.known_frameworks) > 0):
                    self.print('I`m familiar with it too *_*')
                    self.post(ACLMessage.ACCEPT_PROPOSAL, {'known_languages': False, 'experience': False, 'known_frameworks': self.known_frameworks[0]})
                else:
                    self.print('I dont know either')
                    self.post(ACLMessage.ACCEPT_PROPOSAL, {'known_languages': False, 'experience': False, 'known_frameworks': False})
            elif offer:
                if offer > self.salary:
                    self.print('Nice! Deal, see you soon !')
                    self.post(ACLMessage.REJECT_PROPOSAL, {'accept': True})
                else:
                    self.print('Sorry, but I need {} ...'.format(self.salary * 2))
                    self.post(ACLMessage.REJECT_PROPOSAL, {'accept': False})
            else:
                self.print('Anybody !')

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            self.print('See you !')

class Employer(Agent):
    def __init__(self, aid):
        super(Employer, self).__init__(aid=aid, debug=False)
        self.skills = ['PHP', 'C++', 'Java', 'C#']
        self.frameworks = ['.NET', 'Spring']
        self.known_framework = False
        self.known_language = False
        self.experience = False

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def seniority(self, experience):
        if (experience >= 1 and experience < 3):
            return float(1.5)
        elif experience < 1:
            return int(1)
        elif experience >= 3 and experience <= 5:
            return float(2.5)
        elif experience > 5:
            return int(3)

    def experienced_with_framework(self, frameworks):
        if frameworks == ".NET":
            return float(1.2)
        elif frameworks == "JavaFx":
            return float(1.4)
        elif frameworks == "Yii2":
            return float(1.3)
        elif frameworks == "Spring":
            return float(2.1)

    def calculate_price(self, lang):
        if lang == "PHP":
            return int(random.randint(10000, 15000))
        elif lang == "C++":
            return int(random.randint(15000, 25000))
        elif lang == "Java":
            return int(random.randint(23000, 30000))
        elif lang == "C#":
            return int(random.randint(28000, 54000))

    def print(self, msg):
            display_message(self.aid.localname, msg)

    def send_proposal(self):
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="client@localhost:8011"))
        self.send(message)

    def post(self, performative, content):
            message = ACLMessage()
            message.add_receiver(AID(name="client@localhost:8011"))
            message.set_content(json.dumps(content))
            message.set_performative(performative)
            self.send(message)

    def react(self, message):
        super(Employer, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            rand = int(random.randint(1,3))
            needle = self.skills[0:rand]

            self.print("Hello, we currently have a vacancy for a " + "".join(needle))
            self.print("Which of these do you use?")
            self.post(ACLMessage.ACCEPT_PROPOSAL, {'languages': needle, 'frameworks': False, 'offer': False,})

        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)


            experience = content['experience']
            known_language = content['known_languages']
            known_framework = content['known_frameworks']

            if known_language and experience:
                self.experience = content['experience']
                self.known_language = content['known_languages'][0]
                self.print("Good, what about frameworks, do you know " + "".join(self.frameworks))
                self.post(ACLMessage.ACCEPT_PROPOSAL, {'languages': False, 'frameworks': self.frameworks, 'offer': False})

            elif known_framework:
                self.print(known_framework)
                offer = self.calculate_price(self.known_language) * self.seniority(experience) * self.experienced_with_framework(known_framework)
                self.known_framework = content['known_frameworks']
                self.print("Good! Very good!")
                self.print("We can offer you salary {}".format(offer))
                self.post(ACLMessage.ACCEPT_PROPOSAL, {'languages': False, 'frameworks': False, 'offer': offer,})

            elif self.known_language:
                    offer = self.calculate_price(self.known_languages) * self.seniority(self.experience)
                    self.print("We can offer to you {}".format(offer))
                    self.post(ACLMessage.ACCEPT_PROPOSAL, {'languages': False, 'frameworks': False, 'offer': offer,})
            else:
                self.print("Sorry we cant offer any")
                self.post(ACLMessage.ACCEPT_PROPOSAL, {'languages': False, 'frameworks': False, 'offer': False,})

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Good bye!")
            self.post(ACLMessage.REJECT_PROPOSAL, {'accept': False})


if __name__ == '__main__':
    agents = list()

    agent_worker = Worker(AID(name="client@localhost:8011"))
    agent_employer = Employer(AID(name="employer@localhost:8022"))

    agents.append(agent_worker)
    agents.append(agent_employer)


    start_loop(agents)


#[ams@localhost:8000] 09/12/2020 19:35:01.424 --> Agent employer@localhost:8022 successfully identified.
#[client@localhost:8011] 09/12/2020 19:35:01.426 --> Indentification process done.
#[employer@localhost:8022] 09/12/2020 19:35:01.426 --> Indentification process done.
#[client] 09/12/2020 19:35:11.425 --> Hi, I've heard you're looking for developers!
#[employer] 09/12/2020 19:35:11.430 --> Hello, we currently have a vacancy for a PHPC++Java
#[employer] 09/12/2020 19:35:11.430 --> Which of these do you use?
#[client] 09/12/2020 19:35:11.432 --> Sure, I've been worked with it!
#[client] 09/12/2020 19:35:11.432 --> For a 2 years...
#[employer] 09/12/2020 19:35:11.433 --> Good, what about frameworks, do you know .NET, Spring?
#[client] 09/12/2020 19:35:11.435 --> I'm familiar with it too *_*
#[employer] 09/12/2020 19:35:11.436 --> Spring
#[employer] 09/12/2020 19:35:11.436 --> Good! Very good!
#[employer] 09/12/2020 19:35:11.436 --> We can offer you salary 14905.80000000001
#[client] 09/12/2020 19:35:11.437 --> Sorry, but I need 72680...
#[employer] 09/12/2020 19:35:11.439 --> Good bye!
#[client] 09/12/2020 19:35:11.440 --> See you!
