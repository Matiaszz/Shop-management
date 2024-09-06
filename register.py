import sqlite3
from productsCFG import ConfigProducts
from pathlib import Path
from datetime import datetime
import os
TABLE_SELLED = 'Sell'
TABLE_PRODUCTS = 'Produtos'
ROOT = Path(__file__).parent
SQL_FILE = ROOT / 'db.sqlite3'
product_list = []


class Register(ConfigProducts):
    def __init__(self, client: str | None = None, product: str | None = None,
                 qtd: int | None = None, price: float | None = None,
                 date: datetime | None = None):
        super().__init__(client, product, qtd, price, date)

    def _getDate(self, editDate: bool | None = None) -> datetime | None | str:
        print('Data padrão: Dia atual.')
        '''
        This method provides the user with a date or None and prompts them
        if they want to change the date. If they do not want to,
        it returns the current date; otherwise,it gives the option to change
        the date.

        '''
        answerToUserTheDate = self.promptForInput(
            'Quer mudar a data da venda? (s/n): ', ['s', 'n']
        )

        if answerToUserTheDate == 's':
            editDate = True

        if not editDate:
            self.dateDefault = datetime.today()

        else:
            while True:
                try:
                    year = int(input('Digite o ano da compra: '))
                    month = int(input('Digite o mês da compra (1-12): '))
                    day = int(input('Digite o dia da compra (1-31): '))
                    self.dateDefault = datetime(
                        year=year, month=month, day=day)

                    if self.dateDefault > datetime.today():
                        print('Não é possível registrar uma venda '
                              'com data futura.')
                        continue

                    break

                except ValueError:
                    print('Erro ao inserir a data. Por favor, '
                          'insira números válidos.')
                    continue

        formatDate = '%d/%m/%Y'
        self.date = self.dateDefault.strftime(formatDate)

        continueOrCancel = self.promptForInput(
            f'A data será: {self.date}, deseja continuar? (s/n): ', ['s', 'n']
        )

        if continueOrCancel == 's':
            return self.date

        else:
            answerContinueOrNot = self.promptForInput(
                'Deseja refazer a data? (s/n): ', ['s', 'n']
            )

            if answerContinueOrNot == 's':
                return self._getDate()

            else:
                return None

    def _addClient(self) -> str | None:
        while True:
            client = input('Digite o nome do cliente: ').capitalize()
            confirm = self.promptForInput(
                f'Cliente: {client}, deseja prosseguir? (s/n): ', ['s', 'n']
            )
            os.system('cls')

            if confirm == 's':
                return client
            else:
                remake = self.promptForInput(
                    'Gostaria de refazer as informações do cliente (s/n): ', [
                        's', 'n']
                )
                os.system('cls')
                if remake == 's':
                    continue

                else:
                    break

    def registerProduct(self, connection: sqlite3.Connection,
                        cursor: sqlite3.Cursor) -> tuple | None:
        '''
        This method receives a connection to an SQLite3 database
        and uses it to insert the products provided in the inputs
        into a products table in the database.
        '''
        print('REGISTRAR PRODUTO NA BASE DE DADOS')
        try:
            productName = input('Nome do produto: ').capitalize()
            priceProduct = float(input(f'Preço do produto {productName}: '))

            sql = (
                f'INSERT INTO {TABLE_PRODUCTS} (produto, preco) VALUES (?, ?)'
            )
            cursor.execute(sql, (productName, priceProduct))
            connection.commit()
            os.system('cls')
            print('Produto registrado com sucesso')
        except ValueError:
            print('O preço deve ser um número.')
            return

        return productName, priceProduct

    def registerSell(self, connection: sqlite3.Connection,
                     cursor: sqlite3.Cursor):
        """
    Registers a sale by collecting details about the sale and inserting them
    into the database.

    This method performs the following steps:
    1. Prompts the user to input the client's name and confirms it.
    2. Retrieves and displays the list of products from the database.
    3. Allows the user to select multiple products and specify quantities
    for each.
    4. Prompts the user to set or confirm the date of the sale.
    5. Inserts the sale information into the 'Sell' table in the database.

    Parameters:
    - connection (sqlite3.Connection): A connection object to the SQLite3
      database.
    - cursor (sqlite3.Cursor): A cursor object used to execute SQL commands.

    Returns:
    - None: This function does not return any value. It performs database
      operations and prints status messages.

    Raises:
    - ValueError: If the quantity entered is not a valid integer.
    - sqlite3.Error: If there is an error executing the SQL commands.

    Example:
    >>> import sqlite3
    >>> connection = sqlite3.connect('db.sqlite3')
    >>> cursor = connection.cursor()
    >>> registerSell(connection, cursor)
    """
        def createItemDict(product, price, qtd):
            return {'product': product, 'price': price, 'qtd': qtd}

        selledItems = []

        print('---------------------')
        print('REGISTRAR VENDA')
        print('---------------------')
        print()
        self.client = self._addClient()
        if self.client is None:
            return
        product_list.clear()
        _selectProducts(cursor)
        print('Para selecionar múltiplos itens, separe por vírgula.')
        print('Ex: 1,2,3...')

        self.selectItems = input(
            'Quais produtos o cliente '
            f'{self.client} levou?: ').split(',')

        self.selectItems = [int(item.strip()) for item in self.selectItems
                            if item.strip().isdigit()]

        for i in self.selectItems:
            try:
                if 1 <= i <= len(product_list):
                    productSelected = product_list[i-1]['produto']
                    priceSelected = product_list[i-1]['preco']
                    print(f'Produto selecionado: {productSelected}')

                    try:
                        os.system('cls')
                        qtdSelected = int(
                            input(f'Quantidade de ({productSelected})'
                                  ' levados?: '))

                    except ValueError:
                        os.system('cls')
                        print('Digite apenas números.')
                        return

                    selledItems.append(
                        createItemDict(
                            productSelected, priceSelected,
                            qtdSelected
                        )
                    )

                else:
                    print(f'Produto com índice {i} não encontrado.')

            except Exception as e:
                print(f'Erro ao selecionar produto: {e}')

        print()
        os.system('cls')
        date = self._getDate()
        for i in selledItems:
            productSelled = i['product']
            priceSelled = i['price']
            qtdSelled = i['qtd']
            self.add = productSelled, priceSelled, qtdSelled

            if self.client is None or self.add is None or date is None:
                return

            product, price, qtd = self.add

            item = self._viewDict(self.client, product, price, qtd, date)

            sql = (
                f'INSERT INTO {
                    TABLE_SELLED} (cliente, produto, preco, qtd, data) '
                'VALUES (:client, :product, :price, :qtd, :date)'
            )

            try:
                cursor.execute(sql, item)
                connection.commit()

            except sqlite3.Error as e:
                print(f'Erro ao registrar a venda: {e}')
                return

        os.system('cls')
        print('Venda registrada com sucesso!')

    def _viewDict(self, client=None, product=None,
                  price=None, qtd=None, date=None):
        return {
            'client': client,
            'product': product,
            'price': price,
            'qtd': qtd,
            'date': date,
        }


def _selectProducts(cursor: sqlite3.Cursor):
    sql = f'SELECT produto, preco FROM {TABLE_PRODUCTS}'

    def __autoDict(produto, preco):
        return {'produto': produto, 'preco': preco}

    try:
        cursor.execute(sql)
        items = cursor.fetchall()

        for i, item in enumerate(items, start=1):
            produto, preco = item
            product_list.append(__autoDict(produto, preco))
            print(f'{i}. {produto} - R${preco:.2f}')

        return product_list

    except Exception as e:
        print(f'Erro ao buscar produto: {e}')
        return []
