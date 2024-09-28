import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_text_box

class FirstRunUserGearPage:
    def __init__(self, main_window):
        self.main_window = main_window

    def startup(self):
        import helloworld.common.actions as actions

        user_gear_box = toga.Box(style=Pack(direction='column'))

        create_button(box=user_gear_box,
                      action=actions.go_to_start_page,
                      label='Go to Start page',
                      style=Pack(padding=5))

        self.main_window.content = user_gear_box
        self.main_window.show()