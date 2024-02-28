from typing import Optional
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class Currency(Enum):
    USD = "usd"
    CAD = "cad"


target_allocation = {
    "vbr": 0.13, 
    "vti": 0.52,
    "vea": 0.2275,
    "vwo": 0.1225,
}


@dataclass
class Asset:
    """
    override_asset: Designated portfolio assets may not be available in a cooperate RRSP account.
        Use this option to assume the current asset to be a highly correlated portfolio asset. 
    """
    ticker: str
    ttm: float
    price: float
    currency: "Currency"
    override_asset: Optional["Asset"]


@dataclass
class Account:
    name: str
    is_rrsp: bool  # RRSP accounts are dividend efficient, so we should hold higher yield assets
    holdings: dict[str, float]  # lower case tickers and positions, e.g. {"tlt": 50, "ivv": 203.5}
    currency: "Currency"
    contribution_room: Optional[float]  # indicates whether and how much is the contribution room left
    
    def total_value(self, values: dict[str, float]):
        value = 0
        for ticker, quantity in self.holdings.items():
            value += values[ticker] * quantity
        return value
