import json
import sys
from random import randint, choice

from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

import Product


class Seller(Agent):

    __product: Product = None
    __buyer: AID = None

    def __init__(self, aid: str, product: Product, buyer_name: str):
        super(Seller, self).__init__(AID(aid))
        self.__product = product
        self.__buyer = AID(buyer_name)

    def on_start(self):
        super().on_start()

    def react(self, message: ACLMessage):
        super(Seller, self).react(message)
        try:
            if message.performative == ACLMessage.INFORM:
                self.__announce_price()
            elif message.performative == ACLMessage.REJECT_PROPOSAL:
                if self.__product.get_current_price() - self.__product.get_min_price() > 0:
                    self.__reduce_price()
                    self.__announce_price()
                else:
                    self.__refuse_a_deal()
            elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
                self.__sell_product()
        except Exception:
            self.__send_message(ACLMessage.FAILURE, "Internal error.")

    def __announce_price(self):
        self.__send_message(
            ACLMessage.PROPOSE,
            f"I suggest to buy for {self.__product.get_current_price()}.",
            {"price": self.__product.get_current_price()},
        )

    def __reduce_price(self):
        discount: int = randint(
            0, self.__product.get_current_price() - self.__product.get_min_price()
        )
        self.__product.reduce_price_by(discount)

    def __refuse_a_deal(self):
        self.__send_message(
            ACLMessage.REFUSE, "Sorry, but nothing will come of it."
        )

    def __sell_product(self):
        self.__send_message(ACLMessage.AGREE, "Sales!")

    def __say_not_understood(self):
        self.__send_message(
            ACLMessage.NOT_UNDERSTOOD, "I do not understand you."
        )

    def __send_message(
        self, performative: str, displayed_message: str, data: dict = None
    ):
        message = ACLMessage(performative)
        message.add_receiver(self.__buyer)
        if data is not None:
            message.set_content(json.dumps(data))
        display_message(self.aid.localname, displayed_message)
        self.send(message)


if __name__ == "__main__":
    pass
