#У менеджера проекта есть определенный пул задач, которые нужно распределить среди n разработчиков. 
#Для каждой задачи указана сложность и количество дней, на сколько можно отложить задачу. 
#Менеджер приходит к разработчику и просит выполнить одну из задач, в зависимости от приоритета. 
#Разработчик обладает определенными скилами, которые оцениваются значениями. Если разработчик не 
#дотягивает по скилам, то он предлагает подтянуть навыки за определенное время. Если Менеджера 
#устраивает это, то он назначает задачу на данного разработчика, иначе предлагает ему другую задачу. 
#Диалог продолжается, пока не будут опрошены все разработчики. Если не получилось никому назначить задачу, 
#то Менеджер расстраивается и идет к заказчику оправдываться.

import json
import random

from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

PROGRAMMERS_NUMBER = 6

AREA_LIST = ("Kafka", "K8s", "Schema Registry", "Swagger", "Docker", "Avro")

class Manager(Agent):

    def __init__(self, aid):
        super(Manager, self).__init__(aid=aid, debug=False)

        self.tasks = {}
        self.programmer_answers = {}
        self.current_programmer_id = -1

        for task in AREA_LIST:
            difficulty = random.randint(1,10)
            days = random.randint(1, 7)
            self.tasks[task] = {'difficulty': difficulty, 'days': days, 'assignee': None}


    def on_start(self):
        super().on_start()
        self.call_later(10, self.start_dialog)


    def start_dialog(self):
        if (self.current_programmer_id != PROGRAMMERS_NUMBER - 1):
            self.current_programmer_id += 1
            display_message(self.aid.localname, "Привет programmer_{} нужно выполнить задачи.".format(self.current_programmer_id))
            message = ACLMessage()
            message.set_performative(ACLMessage.CONFIRM)
            message.add_receiver(AID(name="programmer_{}@localhost:1022{}".format(self.current_programmer_id, self.current_programmer_id)))
            self.send(message)
        else:
            remaining_task = []
            for task in self.tasks:
                if not self.tasks[task]['assignee']:
                    remaining_task.append(task)

            if len(remaining_task) != 0:
                display_message(self.aid.localname, "Оставшиеся задачи: {}".format(remaining_task))
                display_message(self.aid.localname, "Слабенькие нынче разработчики пошли, придется идти оправдываться перед заказчиком..")

                    
             
    def react(self, message):
        super(Manager, self).react(message)

        programmer_id = self.current_programmer_id

        if message.performative == ACLMessage.PROPOSE:
            message_content = json.loads(message.content)
            task = message_content['task']

            if(int(message_content['days']) > self.tasks[task]['days']):
                display_message(self.aid.localname, "Слишком долго, не подходит.")
                programmer_name = message.sender
                self.programmer_answers[task] = False
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="programmer_{}@localhost:1022{}".format(programmer_id, programmer_id)))
                self.send(message)
            else:
                display_message(self.aid.localname, "Окей, столько времени можно выделить для обучения. Задачу назначаю на тебя.")
                programmer_name = message.sender.localname
                self.tasks[task]['assignee'] = programmer_name
                self.programmer_answers = {}
                self.start_dialog()

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            display_message(self.aid.localname, "Окей, назначаю задачу на тебя.")
            message_content = json.loads(message.content)
            programmer_name = message.sender.localname
            task = message_content['task']
            self.tasks[task]['assignee'] = programmer_name
            self.programmer_answers = {}
            self.start_dialog()

        if message.performative == ACLMessage.CONFIRM:
            programmer_name = message.sender
            flag = False

            for task in self.tasks:
                if (not self.tasks[task]['assignee']) and (not task in self.programmer_answers):
                    flag = True
                    display_message(self.aid.localname, "Как насчет задачи {}?".format(task))
                    content = {'task': task, 'difficulty': self.tasks[task]['difficulty']}
                    message = ACLMessage()
                    message.set_performative(ACLMessage.PROPOSE)
                    message.set_content(json.dumps(content))
                    message.add_receiver(AID(name="programmer_{}@localhost:1022{}".format(programmer_id, programmer_id)))
                    self.send(message)
                    break

            if not flag:
                display_message(self.aid.localname, "Нет задач, подходящих для тебя.")
                message = ACLMessage()
                message.set_performative(ACLMessage.DISCONFIRM)
                message.add_receiver(AID(name="programmer_{}@localhost:1022{}".format(programmer_id, programmer_id)))
                self.send(message)
                self.programmer_answers = {}
                self.start_dialog()


class Programmer(Agent):

    def __init__(self, aid):
        super(Programmer, self).__init__(aid=aid, debug=False)

        self.skills = {}

        for skill in AREA_LIST:
            skill_level = random.randint(1, 10)
            self.skills[skill] = skill_level


    def react(self, message):
        super(Programmer, self).react(message)
        if message.performative == ACLMessage.CONFIRM:
            display_message(self.aid.localname, "Окей, какую задачу я могу взять?")
            message = ACLMessage()
            message.set_performative(ACLMessage.CONFIRM)
            message.add_receiver(AID(name="project_manager@localhost:10230"))
            self.send(message)

        if message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Может я могу взять другую задачу?")
            message = ACLMessage()
            message.set_performative(ACLMessage.CONFIRM)
            message.add_receiver(AID(name="project_manager@localhost:10230"))
            self.send(message)

        if message.performative == ACLMessage.PROPOSE:
            message_content = json.loads(message.content)
            task = message_content['task']
            task_difficulty = message_content['difficulty']

            if task_difficulty > int(self.skills[task]):
                training_time = random.randint(1,10)
                display_message(self.aid.localname, "Сейчас я не могу выполнить задачу {}, но мне нужно {} дней, чтобы подтянуть скиллы.".format(task, training_time))
                content = {'task': task, 'days': training_time}
                message = ACLMessage()
                message.set_sender(self.aid)
                message.set_content(json.dumps(content))
                message.set_performative(ACLMessage.PROPOSE)
                message.add_receiver(AID(name="project_manager@localhost:10230"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Я возьмусь за задачу.")
                content = {'task': task}
                message = ACLMessage()
                message.set_sender(self.aid)
                message.set_content(json.dumps(content))
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="project_manager@localhost:10230"))
                self.send(message)

        if message.performative == ACLMessage.DISCONFIRM:
            display_message(self.aid.localname, "Окей, пойду подтягивать скиллы")


if __name__ == '__main__':
    agents = list()

    project_manager = Manager(AID(name='project_manager@localhost:10230'))
    agents.append(project_manager)
    
    for i in range(PROGRAMMERS_NUMBER):
        agent_programmer = Programmer(AID(name='programmer_{}@localhost:1022{}'.format(i, i)))
        agents.append(agent_programmer)
    
    start_loop(agents)