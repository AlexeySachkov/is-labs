# The seller wants to sell the product at the maximum price.
# The buyer wants to buy the product at the lowest price.
# Goal: negotiate the best price

from pade.misc.utility import start_loop

from Buyer import Buyer
from House import House
from Seller import Seller

BUYER_ID = "buyer@localhost:8008"
SELLER_ID = "seller@localhost:8009"
INITIAL_BUYER_CASH = 350000


if __name__ == "__main__":

    house = House(250000, 500000)

    agents = list()

    buyer = Buyer(BUYER_ID, INITIAL_BUYER_CASH, SELLER_ID)
    seller = Seller(SELLER_ID, house, BUYER_ID)

    agents.append(buyer)
    agents.append(seller)

    start_loop(agents)
