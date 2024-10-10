import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_label
from helloworld.common.handlers.gpt_handler import GptClient

class UserGoalPage:
    def __init__(self, main_window, path):
        self.main_window = main_window
        self.path = path
        self.next_page = 'dev_page'
        self.gpt = GptClient(path=path)

    def startup(self):
        import helloworld.common.actions as actions

        main_box = toga.Box(style=Pack(direction='column'))

        create_label(box=main_box, text=self.gpt.chat_test(), style=Pack(padding=5))

        create_button(box=main_box,
                      action=actions.go_to_dev_page,
                      label='Next',
                      style=Pack(padding=5))

        self.main_window.content = main_box