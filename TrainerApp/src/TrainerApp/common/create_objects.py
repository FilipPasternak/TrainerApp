import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

def create_button(box, action, label, style) -> None:
    box.add(toga.Button(label, on_press=action, style=style))