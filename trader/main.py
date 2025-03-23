import json
from trader.ui import Main, NewOrder, KillOrder, ClosePosition
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
        self.input = None

        yield Header()
        yield Main(ex)
        yield Footer()

    def on_mount(self):
        pass

    def action_close_position(self):
        self.replace_input(ClosePosition(on_submit=ex.close_position))

    def action_kill_order(self):
        self.replace_input(KillOrder(on_submit=ex.kill_order))

    def action_new_order(self):
        self.replace_input(NewOrder(on_submit=ex.place_order))

    def replace_input(self, input):
        if self.input != None:
            self.input.remove()

        self.input = input
        self.screen.mount(input)
        self.refresh()
        pass

    def action_refresh(self):
        self.screen.remove_children()
        self.screen.mount(Header(), Main(ex),Footer())
        self.refresh()

if __name__ == "__main__":
    app = Trader()
    app.title = "Daniel's Happy Trading Terminal"
    app.theme = "dracula"
    app.run()
