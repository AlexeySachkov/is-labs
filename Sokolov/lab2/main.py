"""
Агент Student - студент, который пытается установить и запустить pade
Агент Teacher - преподаватель, который знает как установить pade через консоль и в pyCharm
Student спрашивает Teacher о том, как решить возникшую ошибку.
У Student ошибка возникает с шансом 90%
Когда все возможные ошибки собраны - предлагает альтернативное решение, которое точно сработает
"""
import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
import random

mistakes = {
    "PyCharm": {
        "i haven`t pyCharm": "You must download pyCharm from official website",
        "my pyCharm send error": "Try to reload pyCharm",
        "pade can`t deploy on pyCharm": "Open the terminal and install it",
        "i see only one agent": "Try to open new port for second",
        "something gone wrong": "Ok, try to use Console"
    },
    "Console": {
        "i haven`t python on pc": "Download and setup it",
        "i haven`t pip on pc": "Yeah... download and setup it!",
        "page can`t deploy via console": "Try to pip install page",
        "console crashed": "Ok, try to use PyCharm"
    }
}


class Student(Agent):
    def __init__(self, aid, receiver_aid):
        super(Student, self).__init__(aid=aid, debug=False)
        num = random.randint(0, 1)
        self.env = "PyCharm" if num else "Console"
        self.mistakes = mistakes[self.env]
        self.foundMistakes = []
        self.receiverAID = receiver_aid

    def on_start(self):
        super().on_start()
        self.call_later(10, self.ask_first)

    def send_acl_message(self, attribute, content_json):
        message = ACLMessage()
        message.set_performative(attribute)
        if content_json != 0:
            message.set_content(json.dumps(content_json))
        message.add_receiver(self.receiverAID)
        self.send(message)

    def ask_first(self):
        display_message(self.aid.localname,
                        "I'm try to run program with pade in {}, but something goes wrong. "
                        "Can you help me?".format(self.env))
        self.send_acl_message(ACLMessage.PROPOSE, {'env': self.env})

    def send_mistake(self):
        mistake = ""
        for elem in self.mistakes:
            if elem in self.foundMistakes:
                continue
            else:
                self.foundMistakes.append(elem)
                mistake = elem
                break
        if mistake == "":
            self.send_ok()
        else:
            display_message(self.aid.localname, "Teacher, {}.".format(mistake))
            self.send_acl_message(ACLMessage.QUERY_REF, {'mistake': mistake})

    def send_ok(self):
        display_message(self.aid.localname, "Yes! It`s work!")
        self.send_acl_message(ACLMessage.CONFIRM, 0)

    def is_new_mistake(self):
        have_mistake = random.randint(0, 100)
        if have_mistake < 10:
            self.send_ok()
        else:
            self.send_mistake()

    def react(self, message):
        super(Student, self).react(message)
        if message.performative == ACLMessage.NOT_UNDERSTOOD:
            self.is_new_mistake()
        elif message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Thanks!")
            self.is_new_mistake()
        elif message.performative == ACLMessage.REFUSE:
            display_message(self.aid.localname, "Okay... Thanks anyway.")


class Teacher(Agent):
    def __init__(self, aid, receiver_aid):
        super(Teacher, self).__init__(aid=aid, debug=False)
        self.knownMistakes = mistakes
        self.solvedMistakes = []
        self.env = ""
        self.receiverAID = receiver_aid

    def on_start(self):
        super().on_start()

    def send_acl_message(self, attribute, content_json):
        message = ACLMessage()
        message.set_performative(attribute)
        if content_json != 0:
            message.set_content(json.dumps(content_json))
        message.add_receiver(self.receiverAID)
        self.send(message)

    def ask_about_mistake(self):
        display_message(self.aid.localname, "What is your problem?" if len(self.solvedMistakes) == 0
                                            else "What wrong again?")
        self.send_acl_message(ACLMessage.NOT_UNDERSTOOD, 0)

    def solve_mistake(self, mistake):
        solution = mistakes[self.env][mistake]
        display_message(self.aid.localname, "{}".format(solution))
        self.send_acl_message(ACLMessage.PROPOSE, 0)

    def react(self, message):
        super(Teacher, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            display_message(self.aid.localname, "Okay. Sure. {}".format(content['env']))
            self.ask_about_mistake()
            self.env = content['env']
        elif message.performative == ACLMessage.QUERY_REF:
            content = json.loads(message.content)
            mistake = str(content['mistake'])
            self.solvedMistakes.append(mistake)
            self.solve_mistake(mistake)
        elif message.performative == ACLMessage.CONFIRM:
            display_message(self.aid.localname, "great!")


if __name__ == '__main__':
    agents = list()

    student = Student(AID(name='student@localhost:8022'), receiver_aid=AID(name='teacher@localhost:8011'))
    teacher = Teacher(AID(name='teacher@localhost:8011'), receiver_aid=AID(name='student@localhost:8022'))

    agents.append(student)
    agents.append(teacher)

    start_loop(agents)

"""
[student] 29/11/2020 21:52:48.060 --> I'm try to run program with pade in Console, but something goes wrong. Can you help me?
[teacher] 29/11/2020 21:52:48.060 --> Okay. Sure. Console
[teacher] 29/11/2020 21:52:48.060 --> What is your problem?
[student] 29/11/2020 21:52:48.060 --> Teacher, i haven`t python on pc.
[teacher] 29/11/2020 21:52:48.060 --> Download and setup it
[student] 29/11/2020 21:52:48.060 --> Thanks!
[student] 29/11/2020 21:52:48.060 --> Yes! It`s work!
[teacher] 29/11/2020 21:52:48.060 --> great!

[student] 29/11/2020 21:53:42.761 --> I'm try to run program with pade in PyCharm, but something goes wrong. Can you help me?
[teacher] 29/11/2020 21:53:42.761 --> Okay. Sure. PyCharm
[teacher] 29/11/2020 21:53:42.761 --> What is your problem?
[student] 29/11/2020 21:53:42.761 --> Teacher, i haven`t pyCharm.
[teacher] 29/11/2020 21:53:42.761 --> You must download pyCharm from official website
[student] 29/11/2020 21:53:42.768 --> Thanks!
[student] 29/11/2020 21:53:42.768 --> Teacher, my pyCharm send error.
[teacher] 29/11/2020 21:53:42.768 --> Try to reload pyCharm
[student] 29/11/2020 21:53:42.768 --> Thanks!
[student] 29/11/2020 21:53:42.768 --> Teacher, pade can`t deploy on pyCharm.
[teacher] 29/11/2020 21:53:42.768 --> Open the terminal and install it
[student] 29/11/2020 21:53:42.768 --> Thanks!
[student] 29/11/2020 21:53:42.768 --> Teacher, i see only one agent.
[teacher] 29/11/2020 21:53:42.768 --> Try to open new port for second
[student] 29/11/2020 21:53:42.768 --> Thanks!
[student] 29/11/2020 21:53:42.768 --> Teacher, something gone wrong.
[teacher] 29/11/2020 21:53:42.783 --> Ok, try to use Console
[student] 29/11/2020 21:53:42.783 --> Thanks!
[student] 29/11/2020 21:53:42.783 --> Yes! It`s work!
[teacher] 29/11/2020 21:53:42.783 --> great!

"""