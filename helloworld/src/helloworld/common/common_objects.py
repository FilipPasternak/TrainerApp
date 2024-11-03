from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

class ToggleButton(MDToggleButton, MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)


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