from coinbase.rest import RESTClient

class Exchange():
    DEFAULT_NONE = "-"

    def __init__(self):
        self.client = RESTClient(key_file="/Users/dan/coinbase/api_keys/test-dev.json")

    def positions(self):
        response = self.client.list_futures_positions()
        positions = response.to_dict()["positions"]

        labels = ("ID", "Product", "Side", "Size", "Average", "Profit/Loss")
        rows = []

        for i, p in enumerate(positions):
            rows.append((i + 1, p["product_id"], p["side"], p["number_of_contracts"], p["avg_entry_price"], p["unrealized_pnl"]))

        return [labels, rows]

    def orders(self):
        response = self.client.list_orders(order_status=["OPEN"])
        orders = response.to_dict()["orders"]

        labels = ("ID", "Product", "Side", "Size", "Type", "Limit", "Stop", "Take Profit", "Stop Loss")
        rows = []

        for i, o in enumerate(orders):
            c = list(o["order_configuration"].values())[0]

            rows.append(
                (
                    i + 1,
                    o["product_id"],
                    o["side"],
                    c.get("base_size") or self.DEFAULT_NONE,
                    o["order_type"],
                    c.get("limit_price") or self.DEFAULT_NONE,
                    c.get("stop_trigger_price") or self.DEFAULT_NONE,
                    c.get("take_profit_price") or self.DEFAULT_NONE,
                    c.get("stop_loss_price") or self.DEFAULT_NONE
                )
            )

        return [labels, rows]
