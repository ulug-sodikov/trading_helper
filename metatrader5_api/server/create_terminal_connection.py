from os import getenv

from dotenv import load_dotenv

from metatrader5_terminal_api.metatrader5_terminal_api import MetatraderTerminal


load_dotenv()


def create_terminal_connection():
    mt5_terminal = MetatraderTerminal(getenv("MT5_TERMINAL_PATH"))
    mt5_terminal.connect_to_terminal(
        getenv('MT5_LOGIN'),
        getenv('MT5_PASSWORD'),
        getenv('MT5_SERVER')
    )

    return mt5_terminal
