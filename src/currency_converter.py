from models import Currency

class ForexConverterError(Exception):
    pass


class CurrencyNotAvailableError(ForexConverterError):
    pass


class ForexConverter:
    # TODO: actually fetch the forex rates!
    _rates = {"usd": {"cad": 1.35}}

    def convert(self, base: "Currency", quote: "Currency", amount: float):
        if base in self._rates and quote in self._rates[base]:
            return amount * self._rates[base][quote]
        elif quote in self._rates and base in self._rates[quote]:
            return amount / self._rates[quote][base]
        else:
            raise CurrencyNotAvailableError()
