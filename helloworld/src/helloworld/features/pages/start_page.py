import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from helloworld.common.create_objects import create_button


class StartPage:
    def __init__(self, main_window, path):
        self.main_window = main_window
        self.path = path

    def startup(self):
        import helloworld.common.actions as actions

        main_box = toga.Box(style=Pack(direction=COLUMN))

        create_button(box=main_box,
                      action=actions.go_to_diet_page,
                      label='Go to diet page',
                      style=Pack(padding=5))
        create_button(box=main_box,
                      action=actions.go_to_training_plan_page,
                      label='Go to training plan page',
                      style=Pack(padding=5))

        self.main_window.content = main_box
        self.main_window.show()

