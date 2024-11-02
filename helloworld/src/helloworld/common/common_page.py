import os
import json
from kivy.uix.screenmanager import Screen
# from helloworld.common.handlers.gpt_handler import GptClient


class CommonPage(Screen):
    def __init__(self, path, **kw):
        super().__init__(**kw)
        self.user_data = None
        self.next_page = None
        self.path = path
        # self.gpt_client = GptClient(self.path)

    def save_user_data_and_proceed(self):
        user_data_dict = self.read_json_file('user_data.json')

        for data, value in self.user_data.items():
            user_data_dict[data] = value

        with open(os.path.join(self.path, 'storage', 'user_data.json'), 'w') as file:
            json.dump(user_data_dict, file, indent=4)

        page_methods = {
            'start_page': self.go_to_start_page,
            'diet_page': self.go_to_diet_page,
            'training_plan_page': self.go_to_training_plan_page,
            'place_page': self.go_to_user_place_page,
            'gear_page': self.go_to_user_gear_page,
            'goal_page': self.go_to_user_goal_page,
            'data_page': self.go_to_user_data_page,
            'dev_page': self.go_to_dev_page,
            'settings_page': self.go_to_settings_page
        }
        page_methods[self.next_page]()

    def get_items_from_storage(self, item=None):
        stored_dict = self.read_json_file('user_data.json')
        if item:
            if item in stored_dict:
                return stored_dict[item]
            else:
                return None
        else:
            return stored_dict

    def read_json_file(self, filename: str):
        with open(os.path.join(self.path, 'storage', filename), 'r') as file:
            return json.load(file)

    def add_new_exercise(self, exercise, category, details, place):
        json_files = {
            'Fully equipped gym': os.path.join('exercises', 'full_gym_ex.json'),
            'Only free weights gym': os.path.join('exercises', 'weights_gym_ex.json'),
            'At home with equipment': os.path.join('exercises', 'home_equip_ex.json'),
            'At home without equipment': os.path.join('exercises', 'home_no_equip_ex.json')
        }
        exercises_dict = self.read_json_file(json_files[place])
        exercises_dict[place][category][exercise] = details

        with open(os.path.join(self.path, 'storage', json_files[place]), 'w') as file:
            json.dump(exercises_dict, file, indent=4)

    @staticmethod
    def insert_newlines(text, max_width=500, avg_char_width=10):
        max_chars_per_line = max_width // avg_char_width

        words = text.split(' ')
        current_line_length = 0
        formatted_text = []

        for word in words:
            if current_line_length + len(word) + 1 > max_chars_per_line:
                formatted_text.append('\n')
                current_line_length = 0
            formatted_text.append(word)
            current_line_length += len(word) + 1

        return ' '.join(formatted_text)

    def go_to_start_page(self, *args):
        self.manager.current = 'start_page'

    def go_to_diet_page(self, *args):
        self.manager.current = 'diet_page'

    def go_to_training_plan_page(self, *args):
        self.manager.current = 'generate_plan'

    def go_to_user_place_page(self, *args):
        self.manager.current = 'place_page'

    def go_to_user_gear_page(self, *args):
        self.manager.current = 'gear_page'

    def go_to_user_goal_page(self, *args):
        self.manager.current = 'goal_page'

    def go_to_user_data_page(self, *args):
        self.manager.current = 'data_page'

    def go_to_dev_page(self, *args):
        self.manager.current = 'dev_page'

    def go_to_settings_page(self, *args):
        self.manager.current = 'settings_page'


