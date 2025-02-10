import MetaTrader5 as mt5

from .exceptions import MT5TerminalAPIException


class MetatraderTerminal:
    def __init__(self, path):
        self.path = path

    def connect_to_terminal(self, account_number, password, server):
        """
        Establish a connection with MetaTrader5 terminal.
        """
        # Convert user credentials to proper data types.
        if not mt5.initialize(
            self.path,
            login=int(account_number),
            password=str(password),
            server=str(server)
        ):
            raise MT5TerminalAPIException("Can't connect to MetaTrader5 terminal.")

    def display_account_info(self):
        """
        Display info on current (logged in) trading account.
        """
        info = mt5.account_info()
        if info is None:
            raise MT5TerminalAPIException("Can't get account info.")

        print(
            f'{"-" * 10} Account info {"-" * 10}\n'
            f'Account number:   {info.login}\n'
            f'Balance:          {info.balance} {info.currency}\n'
        )

    def get_last_tick(self, symbol):
        """
        Get the last tick for instrument (symbol).

        Note: Add symbol to MarkerWatch window before getting its tick,
        otherwise None will be returned from mt5.symbol_info_tick(symbol).
        """
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise MT5TerminalAPIException(f"{symbol} is not in MarketWatch window.")

        return tick

    def add_to_marketwatch(self, symbol):
        """
        Add a symbol to the MarketWatch window.
        """
        if not mt5.symbol_select(symbol, True):
            raise MT5TerminalAPIException(f"Can't add {symbol} to MarketWatch window.")

        return True


# TODO: fix imports.
