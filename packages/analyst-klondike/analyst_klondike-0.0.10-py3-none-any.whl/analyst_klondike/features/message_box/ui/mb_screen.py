from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Label, Button
from textual.screen import ModalScreen
from analyst_klondike.state.app_state import AppState, select


class MessageBoxScreen(ModalScreen[bool]):

    @staticmethod
    def message(state: AppState) -> str:
        return state.message_box.message

    CSS_PATH = "mb_screen.tcss"

    def compose(self) -> ComposeResult:
        message = select(MessageBoxScreen.message)
        yield Container(id="shadow")
        with Vertical(id="dialog"):
            yield Label(message)
            with Horizontal(id="buttons"):
                yield Button(id="ok_button",
                             label="ОК",
                             variant="success")

    @on(Button.Pressed, "#ok_button")
    def ok_button_click(self) -> None:
        self.dismiss(True)
