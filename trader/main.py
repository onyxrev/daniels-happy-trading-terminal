import json
from trader.ui import Main, NewOrder
from trader.exchange import Exchange

from textual.app import App
from textual.binding import Binding
from textual.widgets import Header, Footer

ex = Exchange();

class Trader(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="quit"),
        Binding(key="c", action="close_position", description="close position"),
        Binding(key="k", action="kill_order", description="kill order"),
        Binding(key="n", action="new_order", description="new order"),
        Binding(key="r", action="refresh", description="refresh")
    ]

    def compose(self):
        yield Header()
        yield Main(ex)
        yield NewOrder()
        yield Footer()

    def on_mount(self):
        pass

    def action_new(self):
        pass

    def action_refresh(self):
        self.screen.remove_children()
        self.screen.mount(Header(), Main(ex), NewOrder(), Footer())
        self.refresh()

if __name__ == "__main__":
    app = Trader()
    app.title = "Daniel's Happy Trading Terminal"
    app.run()
