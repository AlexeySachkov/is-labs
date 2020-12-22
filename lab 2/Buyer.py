import json
import sys
from random import choice

from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID


class Buyer(Agent):

    cash: int = None
    seller: AID = None

    def __init__(self, aid: str, cash: int, seller_name: str):
        super(Buyer, self).__init__(AID(aid))
        self.cash = cash
        self.seller = AID(seller_name)

    def on_start(self):
        super().on_start()
        self.call_later(
            3,
            lambda: self.send_message(
                ACLMessage.INFORM, "Я хочу купить дом из вашего объявления."
            ),
        )

    def react(self, message: ACLMessage):
        super(Buyer, self).react(message)
        try:
            if message.performative == ACLMessage.PROPOSE:
                if json.loads(message.content)["price"] > self.cash:
                    self.reject_proposal()
                elif choice([True, False]):
                    self.buy_product()
                else:
                    self.refuse_a_deal()
        except Exception:
            self.send_message(ACLMessage.FAILURE, "Internal error.")

    def reject_proposal(self):
        self.send_message(
            ACLMessage.REJECT_PROPOSAL, "."
        )

    def refuse_a_deal(self):
        self.send_message(
            ACLMessage.REFUSE, "Извините, но у нас ничего не получится."
        )

    def buy_product(self):
        self.send_message(ACLMessage.ACCEPT_PROPOSAL, "Мне нравится, я покупаю.")

    def say_not_understood(self):
        self.send_message(
            ACLMessage.NOT_UNDERSTOOD, "Я не понимаю вас."
        )

    def send_message(self, performative: str, displayed_message: str):
        message = ACLMessage(performative)
        message.add_receiver(self.seller)
        display_message(self.aid.localname, displayed_message)
        self.send(message)


if __name__ == "__main__":
    pass
