import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

def create_button(box, action, label, style) -> None:
    box.add(toga.Button(label, on_press=action, style=style))

def create_text_box(box, style):
    ti = toga.TextInput(style=style)
    box.add(ti)
    return ti

def create_label(box, text, style) -> None:
    box.add(toga.Label(text=text, style=style))

def create_switch(box, action, label, style) -> None:
    sw = toga.Switch(text=label, on_change=action, style=style)
    box.add(sw)
    return sw