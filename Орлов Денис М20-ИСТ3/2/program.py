#Выбор старосты в группе
#Агент Chooser - человек, который выдвигает кандидатуру на пост старосты в группе (случайным образом).
#Агент Solver - человек, принимающий решение, основываясь на успеваемости студента.
#Chooser предлагает сделать одного студента старостой -> Solver смотрит на его оценки, и если успеваемость студента
#не удовлетворяет условиям, то Chooser выбирает заново.

import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random

Students = ["Belov","Aparkin","Karenina","Tolstoy","Kolimochkin","Spiridonova","Melnik","Folkin","Galkin","Vdovina","Milova","Samsonova","Morkin"]

Rating = [[4,3,3,4],[5,5,5,5],[3,5,4,4],[4,4,5,4],[5,4,4,3],[2,5,4,4],[4,4,4,4],[4,3,4,5],[4,4,4,2],[4,4,2,4],[4,5,4,4],[4,3,5,4],[3,4,4,4]]

class Chooser(Agent):
    def __init__(self, aid):
        super(Chooser, self).__init__(aid=aid, debug=False)

    def get_Students(self):
        self.studentID = random.randint(0,len(Students)-1)
        self.student = Students[self.studentID]
        display_message(self.aid.localname, Students)

    def on_start(self):
        super().on_start()
        self.call_later(10, self.make_a_choice)

    def make_a_choice(self):
        self.get_Students()
        display_message(self.aid.localname, f"Let {self.student} be the headman!")
        message = ACLMessage()
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'studentID': self.studentID}))
        message.add_receiver(AID(name="solver@localhost:8031"))
        self.send(message)

    def react(self, message):
        super(Chooser, self).react(message)
        answer = json.loads(message.content)
        answerSTR = str(answer['Answer'])
        if (message.performative == ACLMessage.PROPOSE and answerSTR == "Good"):
            display_message(self.aid.localname, f"yay, {self.student} will be the headman!1!")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="solver@localhost:8031"))
            self.send(message)
        elif (message.performative == ACLMessage.PROPOSE and answerSTR == "Bad"):
            display_message(self.aid.localname, "Okey, i choose another one.")
            Students.pop(self.studentID)
            Rating.pop(self.studentID)
            self.make_a_choice()

class Solver(Agent):
    def __init__(self, aid):
        super(Solver, self).__init__(aid=aid, debug=False)

    def on_start(self):
        super().on_start()

    def CheckProgress(self):
        if (3 in Rating[self.choiceID]) or (2 in Rating[self.choiceID]):
            display_message(self.aid.localname, f"{Students[self.choiceID]} has bad rating. We can't choose him. Choose another")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'Answer': "Bad"}))
            message.add_receiver(AID(name="chooser@localhost:8032"))
            self.send(message)
        else:
            display_message(self.aid.localname, f"Okey, we may make {Students[self.choiceID]} the headman.")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'Answer': "Good"}))
            message.add_receiver(AID(name="chooser@localhost:8032"))
            self.send(message)
    
    def react(self, message):
        super(Solver, self).react(message)
        self.students = Students
        self.rating = Rating
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Fine.")
        elif message.performative == ACLMessage.QUERY_REF:
            content = json.loads(message.content)
            self.choiceID = int(content['studentID'])
            self.CheckProgress()

if __name__ == '__main__':
    agents = list()
    solver = Solver(AID(name='solver@localhost:8031'))
    chooser = Chooser(AID(name='chooser@localhost:8032'))
    agents.append(chooser)
    agents.append(solver)
    start_loop(agents)

# [chooser] 21/12/2020 17:08:09.649 --> ['Belov', 'Aparkin', 'Karenina', 'Tolstoy', 'Kolimochkin', 'Spiridonova', 'Melnik', 'Folkin', 'Galkin', 'Vdovina', 'Milova', 'Samsonova', 'Morkin']
# [chooser] 21/12/2020 17:08:09.649 --> Let Vdovina be the headman!
# [solver] 21/12/2020 17:08:09.654 --> Vdovina has bad rating. We can't choose him. Choose another
# [chooser] 21/12/2020 17:08:09.657 --> Okey, i choose another one.
# [chooser] 21/12/2020 17:08:09.657 --> ['Belov', 'Aparkin', 'Karenina', 'Tolstoy', 'Kolimochkin', 'Spiridonova', 'Melnik', 'Folkin', 'Galkin', 'Milova', 'Samsonova', 'Morkin']
# [chooser] 21/12/2020 17:08:09.658 --> Let Belov be the headman!
# [solver] 21/12/2020 17:08:09.663 --> Belov has bad rating. We can't choose him. Choose another
# [chooser] 21/12/2020 17:08:09.666 --> Okey, i choose another one.
# [chooser] 21/12/2020 17:08:09.666 --> ['Aparkin', 'Karenina', 'Tolstoy', 'Kolimochkin', 'Spiridonova', 'Melnik', 'Folkin', 'Galkin', 'Milova', 'Samsonova', 'Morkin']
# [chooser] 21/12/2020 17:08:09.667 --> Let Kolimochkin be the headman!
# [solver] 21/12/2020 17:08:09.671 --> Kolimochkin has bad rating. We can't choose him. Choose another
# [chooser] 21/12/2020 17:08:09.674 --> Okey, i choose another one.
# [chooser] 21/12/2020 17:08:09.674 --> ['Aparkin', 'Karenina', 'Tolstoy', 'Spiridonova', 'Melnik', 'Folkin', 'Galkin', 'Milova', 'Samsonova', 'Morkin']
# [chooser] 21/12/2020 17:08:09.675 --> Let Melnik be the headman!
# [solver] 21/12/2020 17:08:09.678 --> Okey, we may make Melnik the headman.
# [chooser] 21/12/2020 17:08:09.681 --> yay, Melnik will be the headman!1!
# [solver] 21/12/2020 17:08:09.684 --> Fine.
