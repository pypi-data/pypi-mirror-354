"""
Bean-price-compatible price downloader for Vanguard Australia.

Use:

    bean-price -e "AUD:pricedl.beanprice.vanguard_au_detail/HY"
"""

from datetime import datetime

# type: ignore
from beanprice import source
from loguru import logger

from alens.pricedl.model import SecuritySymbol
from alens.pricedl.quotes.vanguard_au_2023_detail import VanguardAu3Downloader


class Source(source.Source):
    """
    Vanguard Australia price source
    ticker: HY
    """

    def get_latest_price(self, ticker) -> source.SourcePrice | None:
        '''
        Downloads the latest price for the ticker.
        '''
        try:
            symbol = ticker

            sec_symbol = SecuritySymbol("VANGUARD", symbol)
            v_price = VanguardAu3Downloader().download(sec_symbol, "")

            price = v_price.value

            min_time = datetime.min.time()
            time = datetime.combine(v_price.date, min_time)
            # The datetime must be timezone aware.
            time = time.astimezone()

            quote_currency = v_price.currency

            return source.SourcePrice(price, time, quote_currency)
        except Exception as e:
            logger.error(e)
            return None

    def get_historical_price(self, ticker, time):
        '''
        Downloads the historical price for the ticker.
        '''
        # todo: return VanguardAu3Downloader().get_historical_price(ticker, time)
        return None
