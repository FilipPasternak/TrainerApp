import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

def create_button(box, action, label, style) -> None:
    button = toga.Button(label, on_press=action, style=style)
    box.add(button)
    return button

def create_text_box(box, style):
    ti = toga.TextInput(style=style)
    box.add(ti)
    return ti

def create_label(box, text, style) -> None:
    box.add(toga.Label(text=text, style=style))

def create_switch(box, action, label, style, add_to_box=True) -> None:
    sw = toga.Switch(text=label, on_change=action, style=style)
    if add_to_box:
        box.add(sw)
    return sw

def create_selection(box, options, on_select):
    sel = toga.Selection(items=options, on_select=on_select)
    box.add(sel)
    return sel
