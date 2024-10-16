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

        with open(os.path.join(self.path, 'storage', 'user_data.json'), 'r') as file:
            user_data_dict = json.load(file)

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
        with open(os.path.join(self.path, 'storage', 'user_data.json'), 'r') as file:
            stored_dict = json.load(file)
        if item:
            if item in stored_dict:
                return stored_dict[item]
            else:
                return None
        else:
            with open(os.path.join(self.path, 'storage', 'user_data.json'), 'r') as file:
                return stored_dict



