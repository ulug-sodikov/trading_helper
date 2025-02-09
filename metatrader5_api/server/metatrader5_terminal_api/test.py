from os import getenv

from dotenv import load_dotenv

from metatrader5_terminal_api import MetatraderTerminal


load_dotenv()


def test():
    metatrader5 = MetatraderTerminal(getenv("MT5_TERMINAL_PATH"))
    metatrader5.connect_to_terminal(
        getenv('MT5_LOGIN'),
        getenv('MT5_PASSWORD'),
        getenv('MT5_SERVER')
    )
    metatrader5.display_account_info()


if __name__ == "__main__":
    test()
