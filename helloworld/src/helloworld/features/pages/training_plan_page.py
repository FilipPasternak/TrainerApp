import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button
from helloworld.common.common_page import CommonPage
from helloworld.common.handlers.gpt_handler import GptClient

class TrainingPlanPage(CommonPage):
    def __init__(self, main_window, path):
        super().__init__(path)
        self.path = path
        self.main_window = main_window
        self.top_label = None

    def startup(self):
        main_box = toga.Box(style=Pack(direction='column'))

        self.top_label = toga.Label('Generate your training plan!', style=Pack(padding=10))
        main_box.add(self.top_label)

        create_button(box=main_box,
                      action=self.generate_plan,
                      label='Generate',
                      style=Pack(padding=5))

        self.main_window.content = main_box

    def generate_plan(self, widget):
        self.top_label.text = 'Generating, please wait...'
        gpt_client = GptClient(self.path)
        stored_data = self.get_items_from_storage()
        plan = gpt_client.generate_plan(stored_data)
