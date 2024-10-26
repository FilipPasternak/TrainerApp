import time

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from helloworld.common.create_objects import create_button, create_label
from helloworld.common.common_page import CommonPage
from helloworld.common.handlers.gpt_handler import GptClient
import os

class TrainingPlanPage(CommonPage):
    def __init__(self, main_window, path):
        super().__init__(path)
        self.path = path
        self.main_window = main_window
        self.top_label = None
        self.plan = None
        self.gpt_client = None
        self.exercises_window = None

    def startup(self):
        main_box = toga.Box(style=Pack(direction='column'))

        self.top_label = toga.Label('Generate your training plan!', style=Pack(padding=10))
        main_box.add(self.top_label)

        create_button(box=main_box,
                      action=self.generate_plan,
                      label='Generate',
                      style=Pack(padding=5))

        create_button(box=main_box,
                      label='Back',
                      action=self.go_to_next_page(page='dev_page'),
                      style=Pack(padding=15, alignment='center'))

        self.main_window.content = main_box

    def generate_plan(self, widget):
        self.top_label.text = 'Generating, please wait...'
        time.sleep(1)
        self.gpt_client = GptClient(self.path)
        stored_user_data = self.get_items_from_storage()
        self.plan = self.gpt_client.generate_plan(stored_user_data)
        self.load_plan(widget=None)

    def load_plan(self, widget):
        new_main_box = toga.Box(style=Pack(direction=COLUMN))

        if not self.plan:
            self.plan = self.read_json_file('workout_plan.json')
        for day, exercises in self.plan.items():
            label = f"{day}: "
            category = list(exercises.keys())
            label += ', '.join(category[:2]) if len(category) == 2 else category[0]

            create_button(new_main_box,
                          label=label,
                          action=self.go_to_exercises)

        create_button(box=new_main_box,
                      label='Back',
                      action=self.go_to_next_page(page='dev_page'),
                      style=Pack(padding=15, alignment='center'))

        self.main_window.content = new_main_box

    def go_to_exercises(self, widget):
        new_main_box = toga.Box(style=Pack(direction=COLUMN))
        day = self.get_day_name_from_label(widget=widget)
        categories = list(self.plan[day].keys())
        exercises = list(self.plan[day].values())

        for i in range(len(categories)):
            create_label(box=new_main_box,
                         text=categories[i])
            exercises_list = exercises[i].split(',')
            for exercise in exercises_list:
                create_button(box=new_main_box,
                              label=exercise.capitalize(),
                              custom_data=categories[i],
                              action=self.go_to_description)

        create_button(box=new_main_box,
                      label='Back',
                      action=self.go_back_to_calendar,
                      style=Pack(padding=15, alignment='center'))
        self.exercises_window = new_main_box
        self.main_window.content = new_main_box

    @staticmethod
    def get_day_name_from_label(widget):
        label_split = widget.text.split(':')
        return label_split[0]

    def go_to_description(self, widget):
        new_main_box = toga.Box(style=Pack(direction=COLUMN))
        category = widget.custom_data
        exercise = widget.text
        details = self.get_exercise_details(category, exercise)
        for item, value in details.items():
            create_label(box=new_main_box,
                         text=f"{item}: \n{self.insert_newlines(text=value, max_width=500)}",
                         style=Pack(width=500, alignment="left", font_size=12, padding=10))

        create_button(box=new_main_box,
                      label='Back',
                      action=self.go_back_to_exercises,
                      style=Pack(padding=15, alignment='center'))

        self.main_window.content = new_main_box

    def get_exercise_details(self, category, exercise):
        place = self.get_items_from_storage(item='Place')
        json_files = {
            'Fully equipped gym': os.path.join('exercises', 'full_gym_ex.json'),
            'Only free weights gym': os.path.join('exercises', 'weights_gym_ex.json'),
            'At home with equipment': os.path.join('exercises', 'home_equip_ex.json'),
            'At home without equipment': os.path.join('exercises', 'home_no_equip_ex.json')
        }
        descriptions = self.read_json_file(filename=json_files[place])
        if exercise in descriptions[place][category]:
            return descriptions[place][category][exercise]
        else:
            details = self.gpt_client.generate_exercise_details(exercise,
                                                                equipment=self.get_items_from_storage(item='User_gear'))
            self.add_new_exercise(exercise, category, details, place)
            return details


    def go_back_to_calendar(self, widget):
        self.load_plan(widget)

    def go_back_to_exercises(self, widget):
        self.main_window.content = self.exercises_window
