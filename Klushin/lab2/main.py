# The seller wants to sell the product at the maximum price.
# The buyer wants to buy the product at the lowest price.
# Goal: negotiate the best price
from pade.misc.utility import start_loop

from Buyer import Buyer
from Product import Product
from Seller import Seller

BUYER_ID = "buyer@localhost:10001"
SELLER_ID = "seller@localhost:10002"
INITIAL_BUYER_CASH = 1200


if __name__ == "__main__":

    product = Product(1000, 2000)

    agents = list()

    buyer = Buyer(BUYER_ID, INITIAL_BUYER_CASH, SELLER_ID)
    seller = Seller(SELLER_ID, product, BUYER_ID)

    agents.append(buyer)
    agents.append(seller)

    start_loop(agents)

"""
Sample:
[buyer] 15/12/2020 18:18:28.353 --> I want to buy a product.
[seller] 15/12/2020 18:18:33.460 --> I suggest to buy for 2000.
[buyer] 15/12/2020 18:18:33.465 --> I am not satisfied with this price.
[seller] 15/12/2020 18:18:33.470 --> I suggest to buy for 1806.
[buyer] 15/12/2020 18:18:33.475 --> I am not satisfied with this price.
[seller] 15/12/2020 18:18:33.480 --> I suggest to buy for 1123.
[buyer] 15/12/2020 18:18:33.484 --> I buy a product!
[seller] 15/12/2020 18:18:33.487 --> Sales!
"""
