import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from helloworld.common.create_objects import create_button


class DevPage:
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
        create_button(box=main_box,
                      action=actions.go_to_start_page,
                      label='Go to start page',
                      style=Pack(padding=5))
        create_button(box=main_box,
                      action=actions.go_to_first_run_user_place_page,
                      label='Go to user place page',
                      style=Pack(padding=5))
        create_button(box=main_box,
                      action=actions.go_to_user_gear_page,
                      label='Go to user gear page',
                      style=Pack(padding=5))
        create_button(box=main_box,
                      action=actions.go_to_user_goal_page,
                      label='Go to user goal page',
                      style=Pack(padding=5))
        create_button(box=main_box,
                      action=actions.go_to_user_data_page,
                      label='Go to user data page',
                      style=Pack(padding=5))

        self.main_window.content = main_box
        self.main_window.show()

