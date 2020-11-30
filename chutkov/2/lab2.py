# "Трудный день"
# Сегодня трудный день для Майкла. Завтра дедлайн, но руководство подкинуло ему несколько задач (10).
# Задачи имеют разный уровень сложности (1 - 10). Всего у Майкла 8 часов на выполенение всех задач.
# Майкл тратит по полчаса на выполнение одной задачи, но в случае провала ему потребуется еще полчаса 
# (16 попыток). Так как в жизни бывает всякое, то и от собранности самого Майкла зависит 
# как просто ему будут даваться задачи. В зависимости от сложности выполненных задач руководитель решит
# увольнять ли Майкла как малоэффективного сотрудника.


import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random


class Employee(Agent):
    def __init__(self, aid, receiver_aid):
        super(Employee, self).__init__(aid=aid, debug=False)
        self.attempts = 16
        self.composure = random.randint(3, 7)
        display_message(self.aid.localname, f"Today Michael's composure = {self.composure}")

        self.receiverAID = receiver_aid
        

    def react(self, message):
        super(Employee, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            task_difficulty = int(content['taskDif'])
            display_message(self.aid.localname, f"Task Difficulty {task_difficulty}")

            if self.attempts == 0:
                display_message(self.aid.localname, "Sorry, boss, I'm done for today")
                self.send_message(0)
            else:
                rate = int(random.randint(self.composure, 10))
                self.attempts = self.attempts - 1
                self.send_message(rate)

    def send_message(self, rate):
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'rate': rate}))
        message.add_receiver(self.receiverAID)
        display_message(self.aid.localname,f"Try: {rate}")
        self.send(message)



class Employer(Agent):
    def __init__(self, aid, receiver_aid):
        super(Employer, self).__init__(aid=aid, debug=False)
        self.receiverAID = receiver_aid
        
    def on_start(self):
        super().on_start()
        display_message(self.aid.localname, 
        "Hey, Micke, we have some real troubles. "
        "Several bugs. We have to fix it TODAY!"
        )
        self.init_tasks()
        self.call_later(10, self.send_task)


    def init_tasks(self):
        self.tasks = []
        self.percent_to_complete = random.randint(50, 100)/100
        display_message(self.aid.localname, f"Employee should complete {self.percent_to_complete*100}% of tasks")

        self.current_tusk_number = 0
        self.sum_tasks_difficulty = 0
        self.sum_of_solved_tasks = 0
        for i in range(10):
            difficulty = random.randint(1, 10)
            self.tasks.append(difficulty)
            self.sum_tasks_difficulty += difficulty
        
    def send_task(self):
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        taskDif = int(self.tasks[self.current_tusk_number])
        message.set_content(json.dumps({'taskDif': taskDif}))
        message.add_receiver(self.receiverAID)
        self.send(message)

    def react(self, message):
        super(Employer, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            rate = int(content['rate'])

            if rate == 0:
                self.calc_result()
                return
            elif rate >= self.tasks[self.current_tusk_number]:
                self.sum_of_solved_tasks = self.sum_of_solved_tasks + self.tasks[self.current_tusk_number]
                self.current_tusk_number = self.current_tusk_number + 1
                if self.current_tusk_number == 10:
                    self.calc_result()
                    return
                else:
                    display_message(self.aid.localname, 
                        "Well done. Task solved. "
                        "So, here is your next task:"
                    )
            else:
                display_message(self.aid.localname, 
                    "Please, try again. We have to fix all bugs today!"
                )
            self.send_task()
    
    def calc_result(self):
        sum = "{:.0f}".format(self.sum_tasks_difficulty*self.percent_to_complete)
        if self.sum_of_solved_tasks >= (self.sum_tasks_difficulty*self.percent_to_complete):
            display_message(self.aid.localname, f"{self.sum_of_solved_tasks} >= {sum}")
            display_message(self.aid.localname, 
                "Okey, you've done your best. "
                "I guess we will sell this product tomorrow"
            )
        else:
            display_message(self.aid.localname, f"{self.sum_of_solved_tasks} < {sum}")
            display_message(self.aid.localname, 
                "It is really bad. We have critical bugs. "
                "No one will buy our product. I'm sorry, but you're fired, Michael"
            )
        


if __name__ == '__main__':

    agents = list()

    employeeName = "Michael@localhost:8011"
    employerName = "Employer@localhost:8022"

    employee = Employee(AID(name=employeeName), receiver_aid=AID(name=employerName))
    employer = Employer(AID(name=employerName), receiver_aid=AID(name=employeeName))

    agents.append(employee)
    agents.append(employer)

    start_loop(agents)


'''
First:
[Michael] 30/11/2020 23:58:40.677 --> Today Michael's composure = 6
[Employer] 30/11/2020 23:58:40.684 --> Hey, Micke, we have some real troubles. Several bugs. We have to fix it TODAY!
[Employer] 30/11/2020 23:58:40.689 --> Employee should complete 89.0% of tasks
[ams@localhost:8000] 30/11/2020 23:58:40.699 --> Agent Michael@localhost:8011 successfully identified.
[ams@localhost:8000] 30/11/2020 23:58:40.700 --> Agent Employer@localhost:8022 successfully identified.
[Michael@localhost:8011] 30/11/2020 23:58:40.702 --> Identification process done.
[Employer@localhost:8022] 30/11/2020 23:58:40.702 --> Identification process done.
[Michael] 30/11/2020 23:58:50.692 --> Task Difficulty 9
[Michael] 30/11/2020 23:58:50.692 --> Try: 9
[Employer] 30/11/2020 23:58:50.695 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.708 --> Task Difficulty 2
[Michael] 30/11/2020 23:58:50.709 --> Try: 10
[Employer] 30/11/2020 23:58:50.712 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.714 --> Task Difficulty 7
[Michael] 30/11/2020 23:58:50.714 --> Try: 9
[Employer] 30/11/2020 23:58:50.717 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.719 --> Task Difficulty 7
[Michael] 30/11/2020 23:58:50.719 --> Try: 8
[Employer] 30/11/2020 23:58:50.721 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.733 --> Task Difficulty 1
[Michael] 30/11/2020 23:58:50.733 --> Try: 6
[Employer] 30/11/2020 23:58:50.735 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.738 --> Task Difficulty 9
[Michael] 30/11/2020 23:58:50.745 --> Try: 7
[Employer] 30/11/2020 23:58:50.748 --> Please, try again. We have to fix all bugs today!
[Michael] 30/11/2020 23:58:50.750 --> Task Difficulty 9
[Michael] 30/11/2020 23:58:50.751 --> Try: 8
[Employer] 30/11/2020 23:58:50.753 --> Please, try again. We have to fix all bugs today!
[Michael] 30/11/2020 23:58:50.755 --> Task Difficulty 9
[Michael] 30/11/2020 23:58:50.762 --> Try: 10
[Employer] 30/11/2020 23:58:50.765 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.767 --> Task Difficulty 4
[Michael] 30/11/2020 23:58:50.767 --> Try: 10
[Employer] 30/11/2020 23:58:50.770 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.772 --> Task Difficulty 7
[Michael] 30/11/2020 23:58:50.779 --> Try: 7
[Employer] 30/11/2020 23:58:50.782 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.784 --> Task Difficulty 7
[Michael] 30/11/2020 23:58:50.784 --> Try: 8
[Employer] 30/11/2020 23:58:50.786 --> Well done. Task solved. So, here is your next task:
[Michael] 30/11/2020 23:58:50.789 --> Task Difficulty 3
[Michael] 30/11/2020 23:58:50.797 --> Try: 7
[Employer] 30/11/2020 23:58:50.799 --> 56 >= 50
[Employer] 30/11/2020 23:58:50.800 --> Okey, you've done your best. I guess we will sell this product tomorrow
'''

'''
Second:
[Michael] 01/12/2020 00:01:07.390 --> Today Michael's composure = 4
[Employer] 01/12/2020 00:01:07.400 --> Hey, Micke, we have some real troubles. Several bugs. We have to fix it TODAY!
[Employer] 01/12/2020 00:01:07.406 --> Employee should complete 56.00000000000001% of tasks
[ams@localhost:8000] 01/12/2020 00:01:07.417 --> Agent Michael@localhost:8011 successfully identified.
[ams@localhost:8000] 01/12/2020 00:01:07.428 --> Agent Employer@localhost:8022 successfully identified.
[Michael@localhost:8011] 01/12/2020 00:01:07.431 --> Identification process done.
[Employer@localhost:8022] 01/12/2020 00:01:07.432 --> Identification process done.
[Michael] 01/12/2020 00:01:17.410 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.410 --> Try: 7
[Employer] 01/12/2020 00:01:17.414 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.431 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.445 --> Try: 4
[Employer] 01/12/2020 00:01:17.448 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.451 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.451 --> Try: 9
[Employer] 01/12/2020 00:01:17.453 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.455 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.456 --> Try: 4
[Employer] 01/12/2020 00:01:17.458 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.460 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.460 --> Try: 6
[Employer] 01/12/2020 00:01:17.462 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.465 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.476 --> Try: 9
[Employer] 01/12/2020 00:01:17.479 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.494 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.494 --> Try: 5
[Employer] 01/12/2020 00:01:17.496 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.511 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.511 --> Try: 10
[Employer] 01/12/2020 00:01:17.514 --> Well done. Task solved. So, here is your next task:
[Michael] 01/12/2020 00:01:17.527 --> Task Difficulty 3
[Michael] 01/12/2020 00:01:17.528 --> Try: 4
[Employer] 01/12/2020 00:01:17.530 --> Well done. Task solved. So, here is your next task:
[Michael] 01/12/2020 00:01:17.544 --> Task Difficulty 3
[Michael] 01/12/2020 00:01:17.544 --> Try: 5
[Employer] 01/12/2020 00:01:17.547 --> Well done. Task solved. So, here is your next task:
[Michael] 01/12/2020 00:01:17.561 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.561 --> Try: 9
[Employer] 01/12/2020 00:01:17.564 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.577 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.578 --> Try: 8
[Employer] 01/12/2020 00:01:17.580 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.594 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.595 --> Try: 6
[Employer] 01/12/2020 00:01:17.597 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.611 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.611 --> Try: 7
[Employer] 01/12/2020 00:01:17.613 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.627 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.628 --> Try: 9
[Employer] 01/12/2020 00:01:17.630 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.644 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.644 --> Try: 6
[Employer] 01/12/2020 00:01:17.647 --> Please, try again. We have to fix all bugs today!
[Michael] 01/12/2020 00:01:17.661 --> Task Difficulty 10
[Michael] 01/12/2020 00:01:17.662 --> Sorry, boss, I'm done for today
[Michael] 01/12/2020 00:01:17.662 --> Try: 0
[Employer] 01/12/2020 00:01:17.664 --> 16 < 34
[Employer] 01/12/2020 00:01:17.675 --> It is really bad. We have critical bugs. No one will buy our product. I'm sorry, but you're fired, Michael
'''
