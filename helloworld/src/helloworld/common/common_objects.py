from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class ToggleButton(MDToggleButton, MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)


class Separator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.width, dp(1))


def popup(title, info):
    dialog_content = info
    close_button = MDRaisedButton(
        text="Close",
        on_release=lambda x: error_dialog.dismiss()
    )
    error_dialog = MDDialog(
        title=title,
        text=dialog_content,
        buttons=[close_button]
    )
    error_dialog.open()

def dropdown(caller, items_list):
    def menu_callback(selected_item):
        caller.text = selected_item
        menu.dismiss()

    menu_items = [
        {
            "text": item,
            "viewclass": "OneLineListItem",
            "height": dp(56),
            "on_release": lambda x=item: menu_callback(x),
        } for item in items_list
    ]

    menu = MDDropdownMenu(
        caller=caller,
        items=menu_items,
        width_mult=4,
    )

    return menu