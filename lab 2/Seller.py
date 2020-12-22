import json
import sys
from random import randint, choice

from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

import House


class Seller(Agent):

    product: House = None
    buyer: AID = None

    def __init__(self, aid: str, product: House, buyer_name: str):
        super(Seller, self).__init__(AID(aid))
        self.product = product
        self.buyer = AID(buyer_name)

    def on_start(self):
        super().on_start()

    def react(self, message: ACLMessage):
        super(Seller, self).react(message)
        try:
            if message.performative == ACLMessage.INFORM:
                self.announce_price()
            elif message.performative == ACLMessage.REJECT_PROPOSAL:
                if self.product.get_current_price() - self.product.get_min_price() > 0:
                    self.reduce_price()
                    self.announce_price()
                else:
                    self.refuse_a_deal()
            elif message.performative == ACLMessage.ACCEPT_PROPOSAL:
                self.sell_product()
        except Exception:
            self.send_message(ACLMessage.FAILURE, "Internal error.")

    def announce_price(self):
        self.send_message(
            ACLMessage.PROPOSE,
            f"Я продаю дом за {self.product.get_current_price()}.",
            {"price": self.product.get_current_price()},
        )

    def reduce_price(self):
        discount: int = randint(
            0, self.product.get_current_price() - self.product.get_min_price()
        )
        self.product.reduce_price_by(discount)

    def refuse_a_deal(self):
        self.send_message(
            ACLMessage.REFUSE, "Извините, ничего не выйдет."
        )

    def sell_product(self):
        self.send_message(ACLMessage.AGREE, "Договорились, мы ждем аванс и готовим документы!")

    def say_not_understood(self):
        self.send_message(
            ACLMessage.NOT_UNDERSTOOD, "Я не понимаю вас."
        )

    def send_message(
            self, performative: str, displayed_message: str, data: dict = None
    ):
        message = ACLMessage(performative)
        message.add_receiver(self.buyer)
        if data is not None:
            message.set_content(json.dumps(data))
        display_message(self.aid.localname, displayed_message)
        self.send(message)


if __name__ == "__main__":
    pass
