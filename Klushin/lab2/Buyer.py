import json
import sys
from random import choice

from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID


class Buyer(Agent):

    __cash: int = None
    __seller: AID = None

    def __init__(self, aid: str, cash: int, seller_name: str):
        super(Buyer, self).__init__(AID(aid))
        self.__cash = cash
        self.__seller = AID(seller_name)

    def on_start(self):
        super().on_start()
        self.call_later(
            3,
            lambda: self.__send_message(
                ACLMessage.INFORM, "I want to buy a product."
            ),
        )

    def react(self, message: ACLMessage):
        super(Buyer, self).react(message)
        try:
            if message.performative == ACLMessage.PROPOSE:
                if json.loads(message.content)["price"] > self.__cash:
                    self.__reject_proposal()
                elif choice([True, False]):
                    self.__buy_product()
                else:
                    self.__refuse_a_deal()
        except Exception:
            self.__send_message(ACLMessage.FAILURE, "Internal error.")

    def __reject_proposal(self):
        self.__send_message(
            ACLMessage.REJECT_PROPOSAL, "I am not satisfied with this price."
        )

    def __refuse_a_deal(self):
        self.__send_message(
            ACLMessage.REFUSE, "Sorry, but nothing will come of it."
        )

    def __buy_product(self):
        self.__send_message(ACLMessage.ACCEPT_PROPOSAL, "I buy a product!")

    def __say_not_understood(self):
        self.__send_message(
            ACLMessage.NOT_UNDERSTOOD, "I do not understand you."
        )

    def __send_message(self, performative: str, displayed_message: str):
        message = ACLMessage(performative)
        message.add_receiver(self.__seller)
        display_message(self.aid.localname, displayed_message)
        self.send(message)


if __name__ == "__main__":
    pass
