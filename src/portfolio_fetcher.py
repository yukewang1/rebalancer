from src.models import Account, Currency, Asset


class Fetcher:
    def fetch_accounts(self):
        raise NotImplementedError()

    def fetch_assets(self):
        raise NotImplementedError()


class MockFetcher(Fetcher):
    def fetch_accounts(self):
        return [
            Account(
                name="IBKR RRSP",
                is_rrsp=True,
                holdings={
                    "ivv": 50,  # unit of this ticker held
                    "tlt": 100,
                    "efa": 25,
                },
                frozen=False,
                currency=Currency.USD,
            ),
            Account(
                name="IBKR TFSA",
                is_rrsp=False,
                holdings={
                    "ivv": 150,
                    "tlt": 200,
                },
                frozen=False,
                currency=Currency.USD,
            ),
        ]

    def fetch_assets(self):
        # tlt, ivv, and efa are considered the "whole universe"
        return [
            Asset(ticker="tlt", dividend_yield=0.0356, price=93.78),
            Asset(ticker="ivv", dividend_yield=0.0141, price=489.82),
            Asset(ticker="efa", dividend_yield=0.0299, price=75.05),
        ]
