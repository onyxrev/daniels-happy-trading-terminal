from textual import on
from textual.containers import VerticalGroup
from textual.widgets import Label, DataTable, Input
from textual.validation import Function, Number, ValidationResult, Validator

class Table(DataTable):
    def __init__(self, labels, rows):
        super().__init__()
        self.cursor_type = None
        self.zebra_stripes = True
        self.add_columns(*labels)
        self.add_rows(rows)

class Main(VerticalGroup):
    def __init__(self, exchange):
        positions_module = PositionsModule(exchange)
        orders_module = OrdersModule(exchange)

        super().__init__(positions_module, orders_module)

class PositionsModule(VerticalGroup):
    def __init__(self, exchange):
        labels, rows = exchange.positions()
        table = Table(labels, rows)

        super().__init__(Label("Positions"), table)

class OrdersModule(VerticalGroup):
    def __init__(self, exchange):
        labels, rows = exchange.orders()
        table = Table(labels, rows)

        super().__init__(Label("Orders"), table)

class NewOrder(VerticalGroup):
    VALID_ORDER_TYPES = ["bl", "bm", "bb", "sl", "sm", "sb"]

    def __init__(self):
        label = Label("New Order")

        order_type = Input(id="new_order", validate_on=["changed"], validators=[Function(self.is_valid, "not valid")])
        order_type.cursor_blink=False

        hint = Label(f"({" ".join(self.VALID_ORDER_TYPES)}) price size take_profit stop_loss")

        super().__init__(label, order_type, hint)

    def pad_list(self, lst, target_length, padding_value=None):
        """Pads a list to a specific length with a padding value."""
        if len(lst) < target_length:
            lst.extend([padding_value] * (target_length - len(lst)))
        return lst

    def parse(self, value: str) -> list[str]:
        try:
            parts = value.strip().split(" ")
        except ValueError:
            parts = []

        if len(parts) > 5:
            return parts[:5]

        return self.pad_list(parts, 5, padding_value=None)


    def is_valid(self, value: str) -> bool:
        order_type, price, size, take_profit, stop_loss = self.parse(value)

        if size == None:
            return False

        if order_type not in self.VALID_ORDER_TYPES:
            return False

        try:
            int(size)
        except(ValueError, TypeError):
            return False

        try:
            if take_profit != None:
                int(take_profit)
        except(ValueError, TypeError):
            return False

        try:
            if stop_loss != None:
                int(stop_loss)
        except(ValueError, TypeError):
            return False

        return True

    @on(Input.Submitted)
    def submit(self, event: Input.Submitted) -> None:
        if event.input.id == "new_order":
            if self.is_valid(value=event.value):
                # TODO: create order
                exit()
