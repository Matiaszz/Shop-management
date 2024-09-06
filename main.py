import sqlite3
import os
from pathlib import Path
from register import Register


TABLE_SELLED = 'Sell'
TABLE_PRODUCTS = 'Produtos'
ROOT = Path(__file__).parent
SQL_FILE = ROOT / 'db.sqlite3'


def createTableProducts(cursor: sqlite3.Cursor):
    sql = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_PRODUCTS} '
        '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'produto TEXT, '
        'preco REAL'
        ')'
    )
    cursor.execute(sql)


def createTableSelled(cursor: sqlite3.Cursor):
    sql = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_SELLED} '
        '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'cliente TEXT, '
        'produto TEXT, '
        'preco REAL, '
        'qtd INTEGER, '
        'data TEXT'
        ')'
    )
    cursor.execute(sql)


def main():
    while True:
        connection = sqlite3.connect(SQL_FILE)
        cursor = connection.cursor()
        register = Register()
        options = {
            '1': lambda: register.registerProduct(connection, cursor),
            '2': lambda: register.registerSell(connection, cursor),
            '3': lambda: exit(),
        }

        try:
            createTableProducts(cursor)
            createTableSelled(cursor)
            print('OPÇÕES: \n 1. Registrar produto \n 2. Registrar Venda \n'
                  ' 3. Sair')

            choice = input('Escolha uma opção: ')
            os.system('cls')

            if choice not in options:
                print('Opção não encontrada.')

            else:
                options[choice]()

        finally:
            cursor.close()
            connection.close()


if __name__ == '__main__':
    main()
