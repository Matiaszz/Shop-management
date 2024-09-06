from datetime import datetime


class Product:
    def __init__(self, client: str | None = None, product: str | None = None,
                 qtd: int | None = None, price: float | None = None,
                 date: datetime | None = None):

        self._date = date
        self._client = client
        self._product = product
        self._qtd = qtd
        self._price = price

    @property
    def dateDefault(self):
        return self._date

    @dateDefault.setter
    def dateDefault(self, value):
        self._date = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value

    @property
    def qtd(self):
        return self._qtd

    @qtd.setter
    def qtd(self, value):
        self._qtd = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value


class ConfigProducts(Product):
    def promptForInput(self, prompt_message: str, valid_responses: list[str]):
        while True:
            response = input(prompt_message).lower().strip()
            if response in valid_responses:
                return response
            print(
                f"Opção inválida. Por favor, escolha"
                f"{' ou '.join(valid_responses)}.")
