class ForexConverter:
    # TODO: actually fetch the currency!
    mock_cad_usd_rate = 0.74

    def convert_usd_to_cad(self, amount: float):
        return amount / self.mock_cad_usd_rate

    def convert_cad_to_usd(self, amount: float):
        return amount * self.mock_cad_usd_rate
