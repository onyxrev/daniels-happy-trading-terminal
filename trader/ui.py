from textual import on
from textual.containers import VerticalGroup
from textual.widgets import Label, DataTable, Input
from textual.validation import Function, Number, ValidationResult, Validator
from typing import Callable

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

class NumberInput(VerticalGroup):
    def __init__(self, on_submit: Callable[[str], None]):
        self.on_submit = on_submit
        label = Label(self.label_text)

        input_node = Input(id=self.input_id, validate_on=["changed"], validators=[Function(self.is_valid, "not valid")])
        input_node.cursor_blink=False

        hint = Label(self.hint_text)

        super().__init__(label, input_node, hint)

    @on(Input.Submitted)
    def submit(self, event: Input.Submitted) -> None:
        if self.is_valid(value=event.value):
            self.on_submit(self.parse(value=event.value))

    def parse(self, value: str) -> list[str]:
        order_id = value.strip()

        try:
            order_id = int(order_id)
        except(ValueError, TypeError):
            return False

        return order_id

    def is_valid(self, value: str) -> bool:
        return self.parse(value) != False

class KillOrder(NumberInput):
    def __init__(self, on_submit: Callable[[str], None]):
        self.label_text = "Kill Order"
        self.hint_text = "order id"
        self.input_id = "kill_order"

        super().__init__(on_submit=on_submit)

class ClosePosition(NumberInput):
    def __init__(self, on_submit: Callable[[str], None]):
        self.label_text = "Close Position"
        self.hint_text = "position id"
        self.input_id = "close_position"

        super().__init__(on_submit=on_submit)

class NewOrder(VerticalGroup):
    VALID_ORDER_TYPES = ["bl", "bm", "bb", "sl", "sm", "sb"]

    def __init__(self, on_submit: Callable[[str, str, str, str, str], None]):
        self.on_submit = on_submit
        label = Label("New Order")

        input_node = Input(id="new_order", validate_on=["changed"], validators=[Function(self.is_valid, "not valid")])
        input_node.cursor_blink=False

        hint = Label(f"({" ".join(self.VALID_ORDER_TYPES)}) price size take_profit stop_loss")

        super().__init__(label, input_node, hint)

    @on(Input.Submitted)
    def submit(self, event: Input.Submitted) -> None:
          if self.is_valid(value=event.value):
              self.on_submit(self.parse(value=event.value))

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
