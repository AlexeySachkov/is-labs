#Два агента- 1 агент Большая компаний, 2 - агент- маленькая компания, стартап.
#Маленькая компания ищет инвестора в обмен на 10% акций.



import json
import random

from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from pade.core.agent import Agent
from pade.misc.utility import display_message, start_loop

class Buyer(Agent):
    def __init__(self, aid, connection):
        super(Buyer, self).__init__(aid=aid, debug=False)
        self.hedge = int(random.randint(1000, 5000000))
        self.metrics = ['gain', 'users', 'earnings']
        self.connection = connection

    def react(self, message):
        super(Buyer, self).react(message)

        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Hello!")
            display_message(self.aid.localname, "How much you growth last month?")
            message = ACLMessage(performative=ACLMessage.PROPOSE)
            message.add_receiver(self.connection)
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            is_start_of_negotiation = content['is_start_of_negotiation']
            if not is_start_of_negotiation:
                random_number = int(random.randint(0, 2))
                random_type = self.metrics[random_number]
                display_message(self.aid.localname, "Let's talk about {}".format(random_type))
                display_message(self.aid.localname, "We can invest {}$".format(self.hedge))
                message = ACLMessage()
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'type': random_type, 'price': 0}))
                message.add_receiver(AID(name="startup@localhost:8022"))
                self.send(message)
            else:
                growth = content['growth']
                price = content['price']
                if self.hedge >= price or (growth and (price / self.hedge < growth / 100)):
                    display_message(self.aid.localname, "We invest, take money")
                    message = ACLMessage()
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    message.set_content(json.dumps({'price': price}))
                    message.add_receiver(AID(name="startup@localhost:8022"))
                    self.send(message)
                else:
                    display_message(self.aid.localname, "To expensive for such valuation")
                    display_message(self.aid.localname, "We can suggest only {}$".format((self.hedge * growth) / 100))
                    message = ACLMessage()
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
                    message.set_content(json.dumps({'price': self.hedge}))
                    message.add_receiver(AID(name="startup@localhost:8022"))
                    self.send(message)
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname, "Thanks, see u")


class Seller(Agent):
    def __init__(self, aid, connection):
        super(Seller, self).__init__(aid=aid, debug=False)
        self.metrics = ['gain', 'users', 'earnings']
        self.connection = connection
        self.type_growth = {}

    def calculate_growth(self):
        return int(random.randint(0, random.randint(1, 5) * 100))

    def calculate_price(self):
        return int(random.randint(1000, 5000000))

    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)

    def send_proposal(self):
        display_message(self.aid.localname, "Hello, we want to sell 10% of company on your investments")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(self.connection)
        self.send(message)

    def react(self, message):
        super(Seller, self).react(message)
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.aid.localname, "Which value u interested in?")
            message = ACLMessage()
            message.set_performative(performative=ACLMessage.ACCEPT_PROPOSAL)
            message.set_content(json.dumps({'is_start_of_negotiation': False}))
            message.add_receiver(self.connection)
            self.send(message)
        elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            if price == 0:
                self.type = content['type']
                self.type_growth[self.type] = self.calculate_growth()
                price_to_sell = self.calculate_price()
                message = ACLMessage(performative=ACLMessage.ACCEPT_PROPOSAL)
                display_message(self.aid.localname, "We growth on {}% last month".format(self.type_growth[self.type]))
                display_message(self.aid.localname, "We want {}$".format(price_to_sell))
                message.set_content(json.dumps({'is_start_of_negotiation': True, 'growth': self.type_growth[self.type], 'price': price_to_sell}))
                message.add_receiver(self.connection)
                self.send(message)
            else:
                display_message(self.aid.localname, "Waiting for your lawyer")
                display_message(self.aid.localname, "See u")
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            content = json.loads(message.content)
            price = content['price']
            min_price = self.calculate_price()
            if min_price <= price:
                display_message(self.aid.localname, "Agreed")
                message = ACLMessage(performative=ACLMessage.ACCEPT_PROPOSAL)
                message.set_content(json.dumps({'is_start_of_negotiation': True, 'price': price, 'growth': self.type_growth[self.type]}))
                message.add_receiver(self.connection)
                self.send(message)
            else:
                display_message(self.aid.localname, "YCombinator always been")
                message = ACLMessage(performative=ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(self.connection)
                self.send(message)


if __name__ == '__main__':
    agents = list()
    buyer_aid = AID(name='huge_company@localhost:8011')
    startup_aid = AID(name="startup@localhost:8022")
    huge_company = Buyer(buyer_aid, startup_aid)
    startup = Seller(startup_aid, buyer_aid)

    agents.append(huge_company)
    agents.append(startup)

    start_loop(agents)

# [startup] 20/12/2020 20:46:29.854 --> Hello, we want to sell 10% of company on your investments
# [huge_company] 20/12/2020 20:46:29.857 --> Hello!
# [huge_company] 20/12/2020 20:46:29.857 --> How much you growth last month?
# [startup] 20/12/2020 20:46:29.861 --> Which value u interested in?
# [huge_company] 20/12/2020 20:46:29.865 --> Let's talk about users
# [huge_company] 20/12/2020 20:46:29.865 --> We can invest 4425456$
# [startup] 20/12/2020 20:46:29.868 --> We growth on 492% last month
# [startup] 20/12/2020 20:46:29.869 --> We want 170041$
# [huge_company] 20/12/2020 20:46:29.872 --> We invest, take money
# [startup] 20/12/2020 20:46:29.877 --> Waiting for your lawyer
# [startup] 20/12/2020 20:46:29.877 --> See u

# [startup] 20/12/2020 20:43:11.234 --> Hello, we want to sell 10% of company on your investments
# [huge_company] 20/12/2020 20:43:11.237 --> Hello!
# [huge_company] 20/12/2020 20:43:11.237 --> How much you growth last month?
# [startup] 20/12/2020 20:43:11.241 --> Which value u interested in?
# [huge_company] 20/12/2020 20:43:11.250 --> Let's talk about gain
# [huge_company] 20/12/2020 20:43:11.250 --> We can invest 2708381$
# [startup] 20/12/2020 20:43:11.255 --> We growth on 42% last month
# [startup] 20/12/2020 20:43:11.255 --> We want 4764347$
# [huge_company] 20/12/2020 20:43:11.260 --> To expensive for such valuation
# [huge_company] 20/12/2020 20:43:11.261 --> We can suggest only 1137520.02$
# [startup] 20/12/2020 20:43:11.267 --> Agreed

# [startup] 20/12/2020 20:55:45.288 --> Hello, we want to sell 10% of company on your investments
# [huge_company] 20/12/2020 20:55:45.291 --> Hello!
# [huge_company] 20/12/2020 20:55:45.291 --> How much you growth last month?
# [startup] 20/12/2020 20:55:45.295 --> Which value u interested in?
# [huge_company] 20/12/2020 20:55:45.300 --> Let's talk about gain
# [huge_company] 20/12/2020 20:55:45.300 --> We can invest 1149503$
# [startup] 20/12/2020 20:55:45.306 --> We growth on 43% last month
# [startup] 20/12/2020 20:55:45.306 --> We want 4781522$
# [huge_company] 20/12/2020 20:55:45.311 --> To expensive for such valuation
# [huge_company] 20/12/2020 20:55:45.311 --> We can suggest only 494286.29$
# [startup] 20/12/2020 20:55:45.316 --> YCombinator always been
# [huge_company] 20/12/2020 20:55:45.322 --> Thanks, see u