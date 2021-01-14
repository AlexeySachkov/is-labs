import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
rand_num = random.randint(0, 3)


class Professor(Agent):
    def __init__(self, aid):
        super(Professor, self).__init__(aid=aid, debug=False)
        self.mark_counter = 0
        self.questions = ["Для чего используется динамическая математическая модель?",
                          "Для чего нужна статическая математическая модель?",
                          "Что такое база знаний?",
                          "Что такое модель?",
                          "Что делает система диагностики?",
                          "Что такое экспертиза?"
                          ]

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Добрый день.")

        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="student@localhost:8080"))
        self.send(message)

    def send_accept(self, q_num):
        display_message(self.aid.localname, self.questions[q_num - 1])
        message = ACLMessage()
        message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
        message.set_content(json.dumps({'questions': q_num}))
        message.add_receiver(AID(name="student@localhost:8080"))
        self.send(message)

    def react(self, message):
        super(Professor, self).react(message)

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            q_ask = content['questions']
            flag = content['flag']
            if q_ask < 6:
                if flag:
                    self.mark_counter += 1 
                self.send_accept(q_ask)

            elif q_ask == 6:
                flag = content['flag']
                message = ACLMessage()
                if flag:
                    self.mark_counter += 1
                display_message(self.aid.localname, "Ваша оценка '{}'".format(self.mark_counter))
                if self.mark_counter < 3:
                    display_message(self.aid.localname, "Добро пожаловать на пересдачу")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                elif self.mark_counter == 5:
                    display_message(self.aid.localname, "Давайте вашу зачетку.")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                else:
                    display_message(self.aid.localname, "Вас устраивает ваша оценка?")
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'questions': q_ask}))
                message.add_receiver(AID(name="student@localhost:8080"))
                self.send(message)
            elif q_ask == 7:
                self.send_accept(q_ask - 1)
            elif q_ask == 8:
                flag = content['flag']
                message = ACLMessage()
                if flag:
                    self.mark_counter += 1
                display_message(self.aid.localname, "Ваша оценка '{}'".format(self.mark_counter))
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="student@localhost:8080"))
                self.send(message)

        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            message = ACLMessage()
            display_message(self.aid.localname, "Давайте вашу зачетку.")
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.add_receiver(AID(name="student@localhost:8080"))
            self.send(message)


class Student(Agent):
    def __init__(self, aid):
        super(Student, self).__init__(aid=aid, debug=False)
        self.ready = ['Да', 'Нет']
        self.answers = ["Она используется для оценки сценариев, которые меняются во времени.",
                        "Она воспроизводит простой 'снимок' ситуации.",
                        "Это знания, необходимые для понимания, формулирования и решения задач.",
                        "Это упрощенное представление или абстракция действительности.",
                        "Включает диагнеостику в медицине, электронике, механике и программном обеспечении.",
                        "Обширное, специфическое знание для решения задачи, извлеченное из обучения, чтения и опыта."
                        ]
        self.no_answer = "Я не знаю ответ на данный вопрос."

    def send_answer(self, q_num, status):
        message = ACLMessage()
        if status == 'Да':
            display_message(self.aid.localname, self.answers[q_num - 2])
            message.set_content(json.dumps({'flag': True, 'questions': q_num}))
        else:
            display_message(self.aid.localname, self.no_answer)
            message.set_content(json.dumps({'flag': False, 'questions': q_num}))
        message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
        message.add_receiver(AID(name="professor@localhost:8090"))
        self.send(message)

    def react(self, message):
        super(Student, self).react(message)
    
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Добрый день, профессор. Я готов.")
            message = ACLMessage()
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'flag': False, 'questions': 1}))
            message.add_receiver(AID(name="professor@localhost:8090"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            q_num = content['questions']
                
            if q_num < 6:
                q_num += 1
                rand_status = self.ready[random.randint(0, 1)]
                self.send_answer(q_num, rand_status)

            elif q_num == 6:
                rand_status = self.ready[random.randint(0, 1)]
                message = ACLMessage()
                if rand_status == 'Да':
                    display_message(self.aid.localname, "Абсолютно устраивает.")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                else:
                    q_num += 1
                    display_message(self.aid.localname, "Я хотел бы повысить оценку.")
                    message.set_content(json.dumps({'flag': False, 'questions': q_num}))
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="professor@localhost:8090"))
                self.send(message)
            elif q_num == 7:
                rand_status = self.ready[random.randint(0, 1)]
                q_num += 1
                self.send_answer(q_num - 1, rand_status)


if __name__ == '__main__':
    agents = list()
    agent_name = 'student@localhost:8080'
    student = Student(AID(name=agent_name))
    professor = Professor(AID(name="professor@localhost:8090"))
    agents.append(student)
    agents.append(professor)
    start_loop(agents)


# Пример №1
# [professor] 23/12/2020 02:42:55.226 --> Добрый день.
# [student] 23/12/2020 02:42:55.228 --> Добрый день, профессор. Я готов.
# [professor] 23/12/2020 02:42:55.231 --> Для чего используется динамическая математическая модель?
# [student] 23/12/2020 02:42:55.234 --> Она используется для оценки сценариев, которые меняются во времени.
# [professor] 23/12/2020 02:42:55.259 --> Для чего нужна статическая математическая модель?
# [student] 23/12/2020 02:42:55.262 --> Она воспроизводит простой 'снимок' ситуации.
# [professor] 23/12/2020 02:42:55.265 --> Что такое база знаний?
# [student] 23/12/2020 02:42:55.267 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:42:55.270 --> Что такое модель?
# [student] 23/12/2020 02:42:55.272 --> Это упрощенное представление или абстракция действительности.
# [professor] 23/12/2020 02:42:55.275 --> Что делает система диагностики?
# [student] 23/12/2020 02:42:55.277 --> Включает диагнеостику в медицине, электронике, механике и программном обеспечении.
# [professor] 23/12/2020 02:42:55.280 --> Ваша оценка '4'
# [professor] 23/12/2020 02:42:55.281 --> Вас устраивает ваша оценка?
# [student] 23/12/2020 02:42:55.305 --> Абсолютно устраивает.
# [professor] 23/12/2020 02:42:55.307 --> Давайте вашу зачетку.

# Пример №2
# [professor] 23/12/2020 02:46:25.787 --> Добрый день.
# [student] 23/12/2020 02:46:25.793 --> Добрый день, профессор. Я готов.
# [professor] 23/12/2020 02:46:25.802 --> Для чего используется динамическая математическая модель?
# [student] 23/12/2020 02:46:25.810 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:46:25.818 --> Для чего нужна статическая математическая модель?
# [student] 23/12/2020 02:46:25.823 --> Она воспроизводит простой 'снимок' ситуации.
# [professor] 23/12/2020 02:46:25.828 --> Что такое база знаний?
# [student] 23/12/2020 02:46:25.832 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:46:25.836 --> Что такое модель?
# [student] 23/12/2020 02:46:25.841 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:46:25.845 --> Что делает система диагностики?
# [student] 23/12/2020 02:46:25.850 --> Включает диагнеостику в медицине, электронике, механике и программном обеспечении.
# [professor] 23/12/2020 02:46:25.854 --> Ваша оценка '2'
# [professor] 23/12/2020 02:46:25.856 --> Добро пожаловать на пересдачу

# Пример №3
# [professor] 23/12/2020 02:51:01.963 --> Добрый день.
# [student] 23/12/2020 02:51:01.969 --> Добрый день, профессор. Я готов.
# [professor] 23/12/2020 02:51:01.976 --> Для чего используется динамическая математическая модель?
# [student] 23/12/2020 02:51:01.985 --> Она используется для оценки сценариев, которые меняются во времени.
# [professor] 23/12/2020 02:51:01.993 --> Для чего нужна статическая математическая модель?
# [student] 23/12/2020 02:51:02.001 --> Она воспроизводит простой 'снимок' ситуации.
# [professor] 23/12/2020 02:51:02.005 --> Что такое база знаний?
# [student] 23/12/2020 02:51:02.009 --> Это знания, необходимые для понимания, формулирования и решения задач.
# [professor] 23/12/2020 02:51:02.012 --> Что такое модель?
# [student] 23/12/2020 02:51:02.016 --> Это упрощенное представление или абстракция действительности.
# [professor] 23/12/2020 02:51:02.019 --> Что делает система диагностики?
# [student] 23/12/2020 02:51:02.022 --> Включает диагнеостику в медицине, электронике, механике и программном обеспечении.
# [professor] 23/12/2020 02:51:02.026 --> Ваша оценка '5'
# [professor] 23/12/2020 02:51:02.026 --> Давайте вашу зачетку.

# Пример №4
# [professor] 23/12/2020 02:51:59.963 --> Добрый день.
# [student] 23/12/2020 02:51:59.969 --> Добрый день, профессор. Я готов.
# [professor] 23/12/2020 02:51:59.976 --> Для чего используется динамическая математическая модель?
# [student] 23/12/2020 02:51:59.986 --> Она используется для оценки сценариев, которые меняются во времени.
# [professor] 23/12/2020 02:51:59.992 --> Для чего нужна статическая математическая модель?
# [student] 23/12/2020 02:51:59.997 --> Она воспроизводит простой 'снимок' ситуации.
# [professor] 23/12/2020 02:52:00.003 --> Что такое база знаний?
# [student] 23/12/2020 02:52:00.007 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:52:00.011 --> Что такое модель?
# [student] 23/12/2020 02:52:00.016 --> Это упрощенное представление или абстракция действительности.
# [professor] 23/12/2020 02:52:00.020 --> Что делает система диагностики?
# [student] 23/12/2020 02:52:00.024 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:52:00.026 --> Ваша оценка '3'
# [professor] 23/12/2020 02:52:00.026 --> Вас устраивает ваша оценка?
# [student] 23/12/2020 02:52:00.029 --> Абсолютно устраивает.
# [professor] 23/12/2020 02:52:00.032 --> Давайте вашу зачетку.

# Пример №5
# [professor] 23/12/2020 02:53:19.557 --> Добрый день.
# [student] 23/12/2020 02:53:19.564 --> Добрый день, профессор. Я готов.
# [professor] 23/12/2020 02:53:19.571 --> Для чего используется динамическая математическая модель?
# [student] 23/12/2020 02:53:19.578 --> Она используется для оценки сценариев, которые меняются во времени.
# [professor] 23/12/2020 02:53:19.584 --> Для чего нужна статическая математическая модель?
# [student] 23/12/2020 02:53:19.588 --> Она воспроизводит простой 'снимок' ситуации.
# [professor] 23/12/2020 02:53:19.593 --> Что такое база знаний?
# [student] 23/12/2020 02:53:19.598 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:53:19.603 --> Что такое модель?
# [student] 23/12/2020 02:53:19.608 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:53:19.612 --> Что делает система диагностики?
# [student] 23/12/2020 02:53:19.617 --> Включает диагнеостику в медицине, электронике, механике и программном обеспечении.
# [professor] 23/12/2020 02:53:19.622 --> Ваша оценка '3'
# [professor] 23/12/2020 02:53:19.623 --> Вас устраивает ваша оценка?
# [student] 23/12/2020 02:53:19.630 --> Я хотел бы повысить оценку.
# [professor] 23/12/2020 02:53:19.635 --> Что такое экспертиза?
# [student] 23/12/2020 02:53:19.639 --> Я не знаю ответ на данный вопрос.
# [professor] 23/12/2020 02:53:19.642 --> Давайте вашу зачетку.


