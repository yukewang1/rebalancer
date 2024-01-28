from typing import List

from src.currency_converter import ForexConverter
from src.models import Account, Currency, Asset
from src.portfolio_fetcher import MockFetcher
import logging

logger = logging.getLogger(__name__)

class AllocatorErrors(Exception):
    pass


class AllocationNotAchievable(AllocatorErrors):
    """
    May occur when allocation is not "best_effort" and some accounts
    are frozen.
    """

    pass


class Allocator:
    def __init__(self):
        self._fetcher = MockFetcher()
        self._accounts: List[Account] = self._fetcher.fetch_accounts()
        self._assets: List[Asset] = self._fetcher.fetch_assets()
        self._fx_converter = ForexConverter()

    def allocate(self, accounts, best_effort=True):
        raise NotImplementedError()

    def assets_field_as_dict(self, field: str):
        price: dict[str, float] = {}
        for asset in self._assets:
            price[asset.ticker] = getattr(asset, field)
        return price

    def get_total_usd_value(self):
        value = 0
        for account in self._accounts:
            account_value = account.total_value(self.assets_field_as_dict("price"))
            value += (
                account_value
                if account.currency == Currency.USD
                else self._fx_converter.convert_cad_to_usd(account_value)
            )
        return value

    def reverse_rank_by_dividends(self):
        """
        Assets with lower dividend yield should be placed into non-RRSP
        accounts first.
        """
        universe = self.assets_field_as_dict("dividend_yield")
        sorted_universe = sorted(universe.items(), key=lambda kv: kv[1])
        logger.info("Reverse dividend ranked universe is %s", sorted_universe)
        return [kv[0] for kv in sorted_universe]


class EqualWeightAllocator(Allocator):
    def __init__(self, target_allocation: dict):
        super().__init__()
        self._target_allocation = target_allocation

    def allocate(self, accounts, best_effort=True):
        pass

    def get_target_percentage_allocation(self):
        allocation = {}
        weight = 1 / len(self._assets)
        for asset in self._assets:
            allocation[asset.ticker] = weight
        return allocation
