class Product(object):
    __MIN_PRICE: int = None
    __ORIGINAL_PRICE: int = None
    __current_price: int = None

    def __init__(self, min_price: int, original_price: int):
        self.__MIN_PRICE = min_price
        self.__ORIGINAL_PRICE = original_price
        self.__current_price = self.__ORIGINAL_PRICE

    def get_min_price(self) -> int:
        return self.__MIN_PRICE

    def get_original_price(self) -> int:
        return self.__ORIGINAL_PRICE

    def get_current_price(self) -> int:
        return self.__current_price

    def reduce_price_by(self, value: int):
        self.__set_new_price(self.__current_price - value)

    def __set_new_price(self, new_price: int):
        if new_price > self.__MIN_PRICE:
            self.__current_price = new_price
        else:
            raise ValueError(
                f"New price ({new_price}) less "
                f"min price ({self.__MIN_PRICE})"
            )
