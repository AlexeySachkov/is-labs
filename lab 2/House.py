class House (object):
    MIN_PRICE: int = None
    ORIGINAL_PRICE: int = None
    current_price: int = None

    def __init__(self, min_price: int, original_price: int):
        self.MIN_PRICE = min_price
        self.ORIGINAL_PRICE = original_price
        self.current_price = self.ORIGINAL_PRICE

    def get_min_price(self) -> int:
        return self.MIN_PRICE

    def get_original_price(self) -> int:
        return self.ORIGINAL_PRICE

    def get_current_price(self) -> int:
        return self.current_price

    def reduce_price_by(self, value: int):
        self.set_new_price(self.current_price - value)

    def __set_new_price(self, new_price: int):
        if new_price > self.MIN_PRICE:
            self.current_price = new_price
        else:
            raise ValueError(
                f"New price ({new_price}) less "
                f"min price ({self.MIN_PRICE})"
            )
