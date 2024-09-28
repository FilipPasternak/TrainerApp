import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from TrainerApp.src.TrainerApp.common.create_objects import create_button


class StartPage:
    def __init__(self, main_window):
        self.main_window = main_window

    def startup(self):
        import TrainerApp.src.TrainerApp.features.actions as actions

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

