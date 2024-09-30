import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_label

class UserGearPage:
    def __init__(self, main_window, path):
        self.main_window = main_window
        self.path = path

    def startup(self):
        import helloworld.common.actions as actions

        main_box = toga.Box(style=Pack(direction='column'))

        create_label(box=main_box, text='Nothing here yet', style=Pack(padding=5))

        create_button(box=main_box,
                      action=actions.go_to_user_goal_page,
                      label='Next',
                      style=Pack(padding=5))

        self.main_window.content = main_box