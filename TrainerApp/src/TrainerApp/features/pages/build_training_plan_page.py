import toga
from toga.style import Pack

class TrainingPlanPage:
    def __init__(self, main_window):
        self.main_window = main_window

    def startup(self):
        import TrainerApp.src.TrainerApp.features.actions as actions

        training_box = toga.Box(style=Pack(direction='column'))

        training_label = toga.Label('This is the training plan Page', style=Pack(padding=10))
        training_box.add(training_label)

        back_button = toga.Button('Back to Start Page', on_press=actions.go_to_start_page, style=Pack(padding=5))
        training_box.add(back_button)

        self.main_window.content = training_box
