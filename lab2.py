#Книжный магазин. Покуптель общается с консультантом в магазине. Договаются о цене.
#происходит выбор книги и оплата
# Клиент здаровается и начинает выбирать книги по жанрам. Когда он собирает то, что хочет оплачивает покупку.
#Если денег не хватает просит скидку.
#
import json
import random
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID


class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
        self.satisfaction = ''
        self.money = 1000
        self.i_want = ['фэнтези','ЛитРПГ','боевое_фэнтези']
        self.bag = []
    def on_start(self):
        super().on_start()
        self.call_later(10, self.apply)
    def apply(self):
        display_message(self.aid.localname, "Добрый день!")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="agent_book_store@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(Client, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            name = content['name']
            if name == "Book_store":
                display_message(self.aid.localname, "Да. Дайте мне пару минут ознакомиться с выставленной литературой")
                number = random.randint(0, len(self.i_want) - 1)
                self.satiety = self.i_want[number]
                display_message(self.aid.localname, "Я хотел бы почитать что-то с {}".format(self.satiety))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'genre': self.i_want[number], 'name': "client", 'price': 0}))
                message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                self.send(message)
            elif name == "seller":
                display_message(self.aid.localname, "Спасибо!")
                self.bag = content['bag']
                display_message(self.aid.localname, "Клиент получил {}".format(self.bag))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                money = 1000 - self.money
                message.set_content(json.dumps({'money': money}))
                message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            flag = content['flag']
            price = content['price']
            message = ACLMessage()
            if flag == 0:
                type_book = content['type']
                self.satiety = type_book
                if self.money >= price:
                    display_message(self.aid.localname, "О! Замечательно. Я куплю!")
                    display_message(self.aid.localname, "Книгу {}".format(type_book))
                    display_message(self.aid.localname, "По цене {}".format(price))
                    self.money -= price
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'name': "client", 'price': price}))
                    message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                    self.send(message)
                elif self.money <= price:
                    display_message(self.aid.localname, "У меня не достаточно денег")
                    display_message(self.aid.localname, "Может сделаете скидку?(")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'cause': "discount", 'price': price}))
                    message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                    self.send(message)
            else:
                if self.money >= price:
                    display_message(self.aid.localname, "Огромное спасибо!! Я покупаю")
                    display_message(self.aid.localname, "Книгу {}".format(self.satiety))
                    display_message(self.aid.localname, "По цене {}".format(price))
                    self.money -= price
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'name': "client", 'price': price}))
                    message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                    self.send(message)
                elif self.money <= price:
                    display_message(self.aid.localname, "У меня не хватает(")
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'cause': "money"}))
                    message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Нет спасибо")
            message.set_performative(ACLMessage.REJECT_PROPOSAL)
            message.set_content(json.dumps({'cause': "end"}))
            message.add_receiver(AID(name="agent_book_store@localhost:8022"))
            self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            ends = content['ends']
            self.bag = content['bag']
            if ends ==1:
                display_message(self.aid.localname, "Нет спасибо. Удачного дня!")
                display_message(self.aid.localname, "Я получил {}".format(self.bag))
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.set_content(json.dumps({'cause': "exactly_the_end"}))
                message.add_receiver(AID(name="agent_book_store@localhost:8022"))
                self.send(message)

class Book_store(Agent):
    def __init__(self, aid):
        super(Book_store, self).__init__(aid=aid, debug=False)

        self.book_list = {'Архимаг': [300, 'боевое_фэнтези'], 'Интервью_с_вампиром': [460,'фэнтези'],
                         'Марш_империи': [500,'альтернативная_история'], 'Мир_и_война': [900,'детектив'],
                        'ИЧЖ': [700,'ЛитРПГ'],'Порог': [410,'фантастика'], '451_по_фарингейту': [1000,'классика'],
                        'Институт': [400,'Мистика']}
        self.buy = []
        self.current_book = ''
    def react(self, message):
        super(Book_store, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Добрый день! Вы что-то хотели?" )
            message = ACLMessage()
            message.set_performative(ACLMessage.PROPOSE)
            message.set_content(json.dumps({'name': 'Book_store'}))
            message.add_receiver(AID(name="agent_client@localhost:8011"))
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            name = content.pop('name')
            message = ACLMessage()
            if price == 0:
                genre = content['genre']
                self.current_book = self.book_search(genre)
                display_message(self.aid.localname, "У нас есть книга в жанре {}".format(genre))
                display_message(self.aid.localname, "Она называется {}".format(self.current_book))
                display_message(self.aid.localname, "Она стоит {}".format(self.menu[self.current_book][0]))
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': format(genre), 'price': self.menu[self.current_book][0], 'flag': 0}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            else:
                display_message(self.aid.localname, "Спасибо за покупку, хотите выбрать другую книгу?")
                self.order.append(self.current_book)
                message.set_performative(ACLMessage.PROPOSE)
                message.set_content(json.dumps({'name': 'Book_store'}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            cause = content['cause']
            message = ACLMessage()
            if cause == 'discount':
                price = content['price']
                display_message(self.aid.localname, "Мы можем скинуть 100")
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                changed_price = price - 100
                message.set_content(json.dumps({'price': changed_price, 'flag': 1}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            elif cause == 'money':
                display_message(self.aid.localname, "Что-то ещё?")
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            elif cause == 'end':
                display_message(self.aid.localname, "Пройдемте на куссу!")
                message.set_performative(ACLMessage.PROPOSE)
                message.set_content(json.dumps({'bag': self.order, 'ends': 1}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
            elif couse == 'exactly_the_end':
                content = json.loads(message.content)
                money = content['money']
                display_message(self.aid.localname, "Приятного чтения!{}".format(money))
                display_message(self.aid.localname, "Спасибо за покупку!")
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'money': money, 'name': 'seller'}))
                message.add_receiver(AID(name="agent_client@localhost:8011"))
                self.send(message)
                

if __name__ == '__main__':
    agents = list()

    agent_client = Client(AID(name="agent_client@localhost:8011"))
    agent_book_store = Book_store(AID(name="agent_book_store@localhost:8022"))

    agents.append(agent_client)
    agents.append(agent_book_store)


    start_loop(agents)

"""
[agent_client] 23/12/2020 19:48:58.073 --> Добрый день!
[agent_book_store] 23/12/2020 19:48:58.131 --> Добрый день! Вы что-то хотели?
[agent_client] 23/12/2020 19:48:58.137 --> Да. Дайте мне пару минут ознакомиться с выставленной литературой 
[agent_client] 23/12/2020 19:48:58.137 --> Я хотел бы почитать что-то с ЛитРПГ
[agent_book_store] 23/12/2020 19:48:58.150 --> У нас есть книга в жанре ЛитРПГ
[agent_book_store] 23/12/2020 19:48:58.150 --> Она называется ИЧЖ
[agent_book_store] 23/12/2020 19:48:58.150 --> Она стоит 700
[agent_client] 23/12/2020 19:48:58.153 --> О! Замечательно. Я куплю!
[agent_client] 23/12/2020 19:48:58.153 --> Книгу ИЧЖ
[agent_client] 23/12/2020 19:48:58.153 --> По цене 700
[agent_book_store] 23/12/2020 19:48:58.156 --> Спасибо за покупку, хотите выбрать другую книгу?
[agent_client] 23/12/2020 19:48:58.160 --> Да. Дайте мне пару минут ознакомиться с выставленной литературой 
[agent_client] 23/12/2020 19:48:58.160 --> Я хотел бы почитать что-то с фэнтези
[agent_book_store] 23/12/2020 19:48:58.163 --> У нас есть книга в жанре фэнтези
[agent_book_store] 23/12/2020 19:48:58.163 --> Она называется Интервью_с_вампиром
[agent_book_store] 23/12/2020 19:48:58.163 --> Она стоит 460
[agent_client] 23/12/2020 19:48:58.166 --> У меня не достаточно денег
[agent_client] 23/12/2020 19:48:58.166 --> Может сделаете скидку?(
[agent_book_store] 23/12/2020 19:48:58.169 --> Мы можем скинуть 100
[agent_client] 23/12/2020 19:48:58.172 --> У меня не хватает(
[agent_book_store] 23/12/2020 19:48:58.175 --> Что-то ещё?
[agent_client] 23/12/2020 19:48:48.177 --> Нет спасибо
[agent_book_store] 23/12/2020 19:58:29.180 --> Пройдемте на куссу!
[agent_client] 23/12/2020 19:48:58.182 --> Нет спасибо. Удачного дня!
[agent_client] 23/12/2020 19:48:58.183 --> Я получил ['ИЧЖ']
[agent_book_store] 23/12/2020 19:48:58.186 --> Приятного чтения!700
[agent_book_store] 23/12/2020 19:48:58.186 --> Спасибо за покупку!
[agent_client] 23/12/2020 19:48:58.189 --> Спасибо!
[agent_client] 23/12/2020 19:48:58.189 --> Клиент получил ['ИЧЖ']
"""
