import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button

class DietPage:
    def __init__(self, main_window, path):
        self.main_window = main_window

    def startup(self):
        import helloworld.common.actions as actions

        main_box = toga.Box(style=Pack(direction='column'))

        diet_label = toga.Label('This is the Diet Page', style=Pack(padding=10))
        main_box.add(diet_label)

        create_button(box=main_box,
                      action=actions.go_to_start_page,
                      label='Go to Start page',
                      style=Pack(padding=5))

        self.main_window.content = main_box


