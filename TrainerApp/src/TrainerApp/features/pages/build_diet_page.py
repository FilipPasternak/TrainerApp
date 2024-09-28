import toga
from toga.style import Pack


class DietPage:
    def __init__(self, main_window):
        self.main_window = main_window

    def startup(self):
        import TrainerApp.src.TrainerApp.features.actions as actions

        diet_box = toga.Box(style=Pack(direction='column'))

        diet_label = toga.Label('This is the Diet Page', style=Pack(padding=10))
        diet_box.add(diet_label)

        back_button = toga.Button('Back to Start Page', on_press=actions.go_to_start_page, style=Pack(padding=5))
        diet_box.add(back_button)

        self.main_window.content = diet_box


