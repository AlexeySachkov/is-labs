"""
•	Агент ZAGS – сообщает ограничение по кол-ву человек на церемони., записывает от молодоженов список гостей на церемонию
•	Агент Newlyweds – молодожены, отбирают гостей на церемонию, сообщают решения ЗАГСу
"""

import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
import random

GUESTS_LIMIT = random.randint(8, 80)

POSSIBLE_GUESTS = [['Молодожены', 2, 5],
                   ['Родители', 4, 5],
                   ['Свидетели', 2, 5],
                   ['Бабушки и дедушки', 4, 4],
                   ['Братья и сестры', 2, 4],
                   ['Крестные', 3, 3],
                   ['Двоюродные братья и сестры', 1, 3],
                   ['Пары свидетелей', 2, 3],
                   ['Родственники', 15, 2],
                   ['Друзья', 12, 1]]


class ZAGS(Agent):
    def __init__(self, aid):
        super(ZAGS, self).__init__(aid=aid, debug=False)
        self.limit = GUESTS_LIMIT

    def on_start(self):
        super().on_start()
        self.call_later(10, self.sending_message)

    def sending_message(self):
        message = ACLMessage()
        message.add_receiver(AID(name="Newlyweds@localhost:8011"))
        message.set_performative(ACLMessage.QUERY_REF)
        message.set_content(json.dumps({'limit': self.limit}))
        display_message(self.aid.localname, "Ограничение кол-ва гостей: {}".format(self.limit))
        self.send(message)

    def accept_guests(self):
        message = ACLMessage()
        message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
        message.add_receiver(AID(name="Newlyweds@localhost:8011"))
        display_message(self.aid.localname, "Отлично, оставляем этих гостей")

    def react(self, message):
        super(ZAGS, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            guests = int(content['guests'])
            is_end = content['is_end']
            display_message(self.aid.localname, "Вы хотите пригласить {} гостей".format(guests))
            message = ACLMessage()
            if is_end == 1:
                self.accept_guests()
            else:
                if guests > self.limit:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="Newlyweds@localhost:8011"))
                    display_message(self.aid.localname, "Гостей больше чем нужно")
                elif guests == self.limit:
                    self.accept_guests()
                elif guests < self.limit:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.add_receiver(AID(name="Newlyweds@localhost:8011"))
                    display_message(self.aid.localname, "Можно пригласить еще гостей")

            self.send(message)


class Newlyweds(Agent):
    def __init__(self, aid):
        super(Newlyweds, self).__init__(aid=aid, debug=False)
        self.guests = 0
        self.limit = 0
        self.index = 0
        self.is_end = 0
        self.invited_guests = []

    def on_start(self):
        super().on_start()

    def send_value(self):
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'guests': self.guests, 'is_end': self.is_end}))
        message.add_receiver(AID(name="ZAGS@localhost:8022"))
        self.send(message)

    def invite_guest(self):
        temp_index = 0
        for row in POSSIBLE_GUESTS:
            temp_index += 1
            if temp_index <= self.index:
                continue

            temp = self.guests + row[1]
            if temp >= self.limit:
                row[1] = self.limit - self.guests
                self.guests = self.limit
            else:
                self.guests += row[1]

            self.invited_guests.append(row)
            self.index += 1

            display_message(self.aid.localname,
                            "Мы пригласим ещё {persons_title}, их будет {persons_count}"
                            .format(persons_title=row[0], persons_count=row[1])
                            )

            if POSSIBLE_GUESTS[-1] == row:
                self.is_end = 1
                if self.limit > self.guests:
                    display_message(self.aid.localname, "На этом наши гости заканчиваются")
            break

        self.send_value()

    def react(self, message):
        super(Newlyweds, self).react(message)

        if message.performative == ACLMessage.QUERY_REF:
            content = json.loads(message.content)
            limit = int(content['limit'])
            self.limit = limit
            self.invite_guest()
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            self.invite_guest()
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            display_message(self.aid.localname, "Отлично!")


if __name__ == '__main__':
    agents = list()

    newlyweds = Newlyweds(AID(name="Newlyweds@localhost:8011"))
    zags = ZAGS(AID(name="ZAGS@localhost:8022"))

    agents.append(newlyweds)
    agents.append(zags)

    start_loop(agents)



"""
Вывод программы:

[ZAGS] 21/12/2020 18:42:10.689 --> Ограничение кол-ва гостей: 25
[Newlyweds] 21/12/2020 18:42:10.692 --> Мы пригласим ещё Молодожены, их будет 2
[ZAGS] 21/12/2020 18:42:10.695 --> Вы хотите пригласить 2 гостей
[ZAGS] 21/12/2020 18:42:10.696 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.699 --> Мы пригласим ещё Родители, их будет 4
[ZAGS] 21/12/2020 18:42:10.701 --> Вы хотите пригласить 6 гостей
[ZAGS] 21/12/2020 18:42:10.702 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.705 --> Мы пригласим ещё Свидетели, их будет 2
[ZAGS] 21/12/2020 18:42:10.708 --> Вы хотите пригласить 8 гостей
[ZAGS] 21/12/2020 18:42:10.709 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.712 --> Мы пригласим ещё Бабушки и дедушки, их будет 4
[ZAGS] 21/12/2020 18:42:10.716 --> Вы хотите пригласить 12 гостей
[ZAGS] 21/12/2020 18:42:10.716 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.719 --> Мы пригласим ещё Братья и сестры, их будет 2
[ZAGS] 21/12/2020 18:42:10.723 --> Вы хотите пригласить 14 гостей
[ZAGS] 21/12/2020 18:42:10.724 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.727 --> Мы пригласим ещё Крестные, их будет 3
[ZAGS] 21/12/2020 18:42:10.730 --> Вы хотите пригласить 17 гостей
[ZAGS] 21/12/2020 18:42:10.730 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.733 --> Мы пригласим ещё Двоюродные братья и сестры, их будет 1
[ZAGS] 21/12/2020 18:42:10.737 --> Вы хотите пригласить 18 гостей
[ZAGS] 21/12/2020 18:42:10.737 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.741 --> Мы пригласим ещё Пары свидетелей, их будет 2
[ZAGS] 21/12/2020 18:42:10.746 --> Вы хотите пригласить 20 гостей
[ZAGS] 21/12/2020 18:42:10.746 --> Можно пригласить еще гостей
[Newlyweds] 21/12/2020 18:42:10.750 --> Мы пригласим ещё Родственники, их будет 5
[ZAGS] 21/12/2020 18:42:10.754 --> Вы хотите пригласить 25 гостей
[ZAGS] 21/12/2020 18:42:10.754 --> Отлично, оставляем этих гостей

"""
