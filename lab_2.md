# Найм

#идет найм сотрудника, и встает вопрос о заработной плате, работодатель и потенциальный сотрудник договариваются о размере зп исходя из его опыта

```
import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
rand_num=random.randint(0,3)
class Employer(Agent):
    def __init__(self, aid):
        super(Employer, self).__init__(aid=aid, debug=False)
        self.status = ['student', 'junior', 'middle', 'senior']
        self.st = ''

    def offer(self):
        if self.st == "student":
            return int(random.randint(10, 20))
        elif self.st == "junior":
            return int(random.randint(15, 30))
        elif self.st == "middle":
            return int(random.randint(35, 70))
        elif self.st == "senior":
            return int(random.randint(55, 160))

    def e_zp(self):
        if self.st == "student":
            return 10
        elif self.st == "junior":
            return 15
        elif self.st == "middle":
            return 35
        elif self.st == "senior":
            return 55

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Есть ли у вас какие-нибудь вопросы?")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="worker@localhost:8011"))
        self.send(message)

    def react(self, message):
        super(Employer, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Какой у вас уровень и на какую з/п вы претендуете?")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'flag': False}))
            message.add_receiver(AID(name="worker@localhost:8011"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            zp = content['zp']
            if zp == 0:
                self.st = content['st']
                zp = self.offer()
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                display_message(self.aid.localname, "Мы готовы предложить вам {} 000".format(zp))
                message.set_content(json.dumps({'flag': True, 'zp': zp}))
                message.add_receiver(AID(name="worker@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Договорились! Ваша зарплата составит {} 000".format(zp))
                display_message(self.aid.localname, "Добро пожаловать в кампанию!")

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            zp = content['zp']
            e_zp = self.e_zp()
            if e_zp <= zp+5:
                display_message(self.aid.localname, "Окей, вы нам нравитесь")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'flag': True, 'zp': zp}))
                message.add_receiver(AID(name="worker@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Извините, вы нам не подходите")
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="worker@localhost:8011"))
                self.send(message)

class Worker(Agent):
    def __init__(self, aid):
        super(Worker, self).__init__(aid=aid, debug=False)
        self.status = ['student', 'junior', 'middle', 'senior']
        if rand_num == 0:
            self.zp = int(random.randint(10, 30))
        elif rand_num == 1:
            self.zp = int(random.randint(10, 35))
        elif rand_num == 2:
            self.zp = int(random.randint(35, 80))
        elif rand_num == 3:
            self.zp = int(random.randint(55, 180))

    def react(self, message):
        super(Worker, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Я хотел бы обсудить размер зарплаты")
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.add_receiver(AID(name="employer@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            if not flag :
                rand_status = self.status[rand_num]
                display_message(self.aid.localname, "Мой уровень {} ".format(rand_status))
                display_message(self.aid.localname, "Я претендую на з/п {} 000".format(self.zp))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'st': rand_status, 'zp': 0}))
                message.add_receiver(AID(name="employer@localhost:8022"))
                self.send(message)
            else:
                zp = content['zp']
                if self.zp <= zp:
                    display_message(self.aid.localname, "Это прекрасно)")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'zp': zp}))
                    message.add_receiver(AID(name="employer@localhost:8022"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "Я уверен, что моего уровня достаточно для {} 000".format(self.zp))
                    message = ACLMessage()
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'zp': self.zp}))
                    message.add_receiver(AID(name="employer@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Тогда всего хорошего!")


if __name__ == '__main__':
    agents = list()

    agent_name = 'worker@localhost:8011'
    worker = Worker(AID(name=agent_name))
    employer = Employer(AID(name="employer@localhost:8022"))

    agents.append(worker)
    agents.append(employer)


    start_loop(agents)

#возможные варианты развития событий
#[employer] 07/12/2020 21:39:16.435 --> Есть ли у вас какие-нибудь вопросы?
#[worker] 07/12/2020 21:39:16.445 --> Я хотел бы обсудить размер зарплаты
#[employer] 07/12/2020 21:39:16.459 --> Какой у вас уровень и на какую з/п вы претендуете?
#[worker] 07/12/2020 21:39:16.474 --> Мой уровень student
#[worker] 07/12/2020 21:39:16.475 --> Я претендую на з/п 13 000
#[employer] 07/12/2020 21:39:16.484 --> Мы готовы предложить вам 13 000
#[worker] 07/12/2020 21:39:16.492 --> Это прекрасно)
#[employer] 07/12/2020 21:39:16.499 --> Договорились! Ваша зарплата составит 13 000
#[employer] 07/12/2020 21:39:16.500 --> Добро пожаловать в кампанию!

#[employer] 07/12/2020 21:42:26.050 --> Есть ли у вас какие-нибудь вопросы?
#[worker] 07/12/2020 21:42:26.060 --> Я хотел бы обсудить размер зарплаты
#[employer] 07/12/2020 21:42:26.076 --> Какой у вас уровень и на какую з/п вы претендуете?
#[worker] 07/12/2020 21:42:26.088 --> Мой уровень middle
#[worker] 07/12/2020 21:42:26.088 --> Я претендую на з/п 49 000
#[employer] 07/12/2020 21:42:26.101 --> Мы готовы предложить вам 41 000
#[worker] 07/12/2020 21:42:26.112 --> Я уверен, что моего уровня достаточно для 49 000
#[employer] 07/12/2020 21:42:26.121 --> Извините, вы нам не подходите
#[worker] 07/12/2020 21:42:26.131 --> Тогда всего хорошего!

#[employer] 07/12/2020 21:51:19.409 --> Есть ли у вас какие-нибудь вопросы?
#[worker] 07/12/2020 21:51:19.420 --> Я хотел бы обсудить размер зарплаты
#[employer] 07/12/2020 21:51:19.436 --> Какой у вас уровень и на какую з/п вы претендуете?
#[worker] 07/12/2020 21:51:19.448 --> Мой уровень senior
#[worker] 07/12/2020 21:51:19.449 --> Я претендую на з/п 128 000
#[employer] 07/12/2020 21:51:19.460 --> Мы готовы предложить вам 158 000
#[worker] 07/12/2020 21:51:19.469 --> Это прекрасно)
#[employer] 07/12/2020 21:51:19.477 --> Договорились! Ваша зарплата составит 158 000
#[employer] 07/12/2020 21:51:19.477 --> Добро пожаловать в кампанию!

#[employer] 07/12/2020 22:11:35.091 --> Есть ли у вас какие-нибудь вопросы?
#[worker] 07/12/2020 22:11:35.101 --> Я хотел бы обсудить размер зарплаты
#[employer] 07/12/2020 22:11:35.116 --> Какой у вас уровень и на какую з/п вы претендуете?
#[worker] 07/12/2020 22:11:35.131 --> Мой уровень middle
#[worker] 07/12/2020 22:11:35.132 --> Я претендую на з/п 75 000
#[employer] 07/12/2020 22:11:35.152 --> Мы готовы предложить вам 62 000
#[worker] 07/12/2020 22:11:35.167 --> Я уверен, что моего уровня достаточно для 75 000
#[employer] 07/12/2020 22:11:35.182 --> Окей, вы нам нравитесь
#[worker] 07/12/2020 22:11:35.199 --> Это прекрасно)
#[employer] 07/12/2020 22:11:35.213 --> Договорились! Ваша зарплата составит 75 000
#[employer] 07/12/2020 22:11:35.214 --> Добро пожаловать в кампанию!

```
