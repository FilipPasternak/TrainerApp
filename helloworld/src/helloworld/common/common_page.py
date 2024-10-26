import toga
import os
import csv
import json


class CommonPage:
    def __init__(self, path):
        self.user_data = None
        self.next_page = None
        self.path = path

    def save_user_data_and_proceed(self, widget):
        import helloworld.common.actions as actions

        user_data_dict = self.read_json_file('user_data.json')

        for data, value in self.user_data.items():
            user_data_dict[data] = value

        with open(os.path.join(self.path, 'storage', 'user_data.json'), 'w') as file:
            json.dump(user_data_dict, file, indent=4)

        if self.next_page == 'user_place':
            actions.go_to_first_run_user_place_page(widget=widget)
        elif self.next_page == 'user_gear':
            actions.go_to_user_gear_page(widget=widget)
        elif self.next_page == 'user_goal':
            actions.go_to_user_goal_page(widget=widget)
        elif self.next_page == 'dev_page':
            actions.go_to_dev_page(widget=widget)

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
    def go_to_next_page(page):
        import helloworld.common.actions as actions
        goto_functions = {
            'user_place': actions.go_to_first_run_user_place_page,
            'user_gear': actions.go_to_user_gear_page,
            'user_goal': actions.go_to_user_goal_page,
            'dev_page': actions.go_to_dev_page
        }
        return goto_functions[page]

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
