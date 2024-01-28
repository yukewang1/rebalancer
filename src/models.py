import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class Currency(Enum):
    USD = "usd"
    CAD = "cad"


@dataclass
class Asset:
    ticker: str
    dividend_yield: float
    price: float
    currency: "Currency" = Currency.USD


@dataclass
class Account:
    name: str
    is_rrsp: bool  # RRSP accounts are dividend efficient, so we should hold higher yield assets
    holdings: dict[str, float]  # lower case ticker, e.g. {"tlt": 50.35, "ivv": 200.3}
    frozen: bool  # no allocation change allowed
    currency: "Currency" = Currency.USD

    def total_value(self, values: dict[str, float]):
        value = 0
        for ticker, quantity in self.holdings.items():
            value += values[ticker] * quantity
        return value
