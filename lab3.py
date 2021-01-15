#Зачада состоит в следующем
#HR-специалист компании проводит собеседование на определенную вакансию
#Представим, что все кандидаты имеют примерно одинаковые скиллы
#Поэтому стоит вопрос только зп, тк ресурсы у компании ограничены
#Нужно опросить каждого кандидата и выбрать того, кто удовлетворяет интересам компании

import random

from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

candidate_count = 10

class Manager(Agent):

    def __init__(self, aid):
        super(Manager, self).__init__(aid=aid, debug=False)
        self.min_wade = random.randint(1000, 1900)
        self.max_wade = random.randint(1900, 2300)
        self.current_candidate = -1

    def on_start(self):
        super().on_start()
        self.call_later(10, self.start_dialog)

    def start_dialog(self):
        if self.current_candidate != candidate_count - 1:
            self.current_candidate += 1
            display_message(self.aid.localname, "Привет candidate_{}! Хочешь работать у нас в компании? "
                                                "У нас офис в центре города и автобус от компании!"
                            .format(self.current_candidate))
            message = ACLMessage()
            message.set_performative(ACLMessage.CONFIRM)
            message.add_receiver(AID(name="candidate_{}@localhost:1022{}".format(self.current_candidate, self.current_candidate)))
            self.send(message)
        else:
            display_message(self.aid.localname, "Жаль, но так и не получилось найти кандидата, "
                                                "который нас устраиваивает по всем параметрам :(")

    def react(self, message):
        super(Manager, self).react(message)

        candidate_id = self.current_candidate
        
        if message.performative == ACLMessage.CONFIRM:
            display_message(self.aid.localname, "На данный момент мы готовы предложить тебе {}$."
                                                "Тебя устраивает такая зп или будем торговаться как на рынке?"
                                                .format(self.min_wade))
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(int(self.min_wade))
            message.add_receiver(AID(name="candidate_{}@localhost:1022{}".format(candidate_id, candidate_id)))
            self.send(message)

        if message.performative == ACLMessage.PROPOSE:
            if int(message.content) > self.max_wade:
                display_message(self.aid.localname, "Извините, но мы не готовы столько платить! "
                                                    "Максимум, что мы гововы Вам предложить это {}$ "
                                                    "+ бесплатный кофе и печеньки".format(self.max_wade))
                message = ACLMessage()
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.set_content(int(self.max_wade))
                message.add_receiver(AID(name="candidate_{}@localhost:1022{}".format(candidate_id, candidate_id)))
                self.send(message)
            else:
                display_message(self.aid.localname, "Да, окей! Мы согласны! Ты принят на работу!")
                display_message(self.aid.localname, "Мы нашли нашего кандидата! Это candidate №{}"
                                .format(candidate_id))

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            display_message(self.aid.localname, "Да, окей! Мы согласны! Ты принят на работу!")

        if message.performative == ACLMessage.DISCONFIRM:
            self.start_dialog()

class Programmer(Agent):

    def __init__(self, aid):
        super(Programmer, self).__init__(aid=aid, debug=False)
        self.wanted_wade = random.randint(1800, 3000)

    def react(self, message):
        super(Programmer, self).react(message)
        if message.performative == ACLMessage.CONFIRM:
            display_message(self.aid.localname, "Да, хочу работать у вас. Но какую зп вы можете мне предложить?")
            message = ACLMessage()
            message.set_performative(ACLMessage.CONFIRM)
            message.add_receiver(AID(name="рк@localhost:10230"))
            self.send(message)

        if message.performative == ACLMessage.PROPOSE:
            if int(message.content) < self.wanted_wade:
                display_message(self.aid.localname, "Нет, это очень мало :( Я же не на стажера пришел устраиватся... "
                                                    "Я хочу {}$ и чтобы было ДМС и карта в спорт клуб! "
                                                    "И премии квартальные...".format(self.wanted_wade))
                message = ACLMessage()
                message.set_performative(ACLMessage.PROPOSE)
                message.add_receiver(AID(name="project_manager@localhost:10230"))
                message.set_content(int(self.wanted_wade))
                self.send(message)
            else:
                display_message(self.aid.localname, "Это не критично для меня. "
                                                    "Главное - дружная команда и интересный проект! Я согласен!")

        if message.performative == ACLMessage.REJECT_PROPOSAL:
            if int(message.content) - self.wanted_wade > 100:
                display_message(self.aid.localname, "Это не критично для меня. "
                                                    "Главное - дружная команда и интересный проект! Я согласен!")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="project_manager@localhost:10230"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Не, ребята, ищите дурака! Меня в другую компанию "
                                                    "с руками и ногами заберут на хорошую зп! Пока-пока!")
                message = ACLMessage()
                message.set_performative(ACLMessage.DISCONFIRM)
                message.add_receiver(AID(name="hr@localhost:10230"))
                self.send(message)

if __name__ == '__main__':
    agents = list()

    project_manager = Manager(AID(name='hr@localhost:10230'))
    agents.append(project_manager)

    for i in range(candidate_count):
        agent_programmer = Programmer(AID(name='candidate_{}@localhost:1022{}'.format(i, i)))
        agents.append(agent_programmer)

    start_loop(agents)