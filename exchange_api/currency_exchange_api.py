import requests as req
import re


def get_exchange_rate():
    """
    Get current exchange rate to dollar-ruble.
    :return: exchange rate.
    """
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    r = req.get(url)
    exchange_rate_value_regex = re.compile(r'<Valute ID="R01235"><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal><Name>Доллар США</Name><Value>([^"]*)</Value></Valute>')
    exchange_rate_value_match = exchange_rate_value_regex.search(r.text)
    if exchange_rate_value_match is None:
        return None
    exchange_rate_value = exchange_rate_value_match.group(1)
    return float(exchange_rate_value.replace(',', '.'))


def convert_dollars_in_rubles(exchange_rate, cost_in_dollars):
    """
    Convert cost in dollars to cost in rubles.
    :param exchange_rate: exchange rate.
    :param cost_in_dollars: cost from Google Sheet.
    :return: cost in rubles.
    """
    return float(format(exchange_rate * cost_in_dollars, '.2f'))

