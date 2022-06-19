import requests as req
import re


def get_exchange_rate():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    r = req.get(url)
    exchange_rate_value_regex = re.compile(r'<Valute ID="R01235"><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal><Name>Доллар США</Name><Value>([^"]*)</Value></Valute>')
    exchange_rate_value_match = exchange_rate_value_regex.search(r.text)
    if exchange_rate_value_match is None:
        return None
    exchange_rate_value = exchange_rate_value_match.group(1)
    return float(exchange_rate_value.replace(',', '.'))


def convert_dollars_in_rubles(exchange_rate, cost_in_dollars):
    return float(format(exchange_rate * cost_in_dollars, '.2f'))

