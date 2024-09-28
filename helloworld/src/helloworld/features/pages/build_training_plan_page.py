import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button

class TrainingPlanPage:
    def __init__(self, main_window, path):
        self.main_window = main_window

    def startup(self):
        import helloworld.common.actions as actions

        training_box = toga.Box(style=Pack(direction='column'))

        training_label = toga.Label('This is the training plan Page', style=Pack(padding=10))
        training_box.add(training_label)

        create_button(box=training_box,
                      action=actions.go_to_start_page,
                      label='Go to Start page',
                      style=Pack(padding=5))

        self.main_window.content = training_box
