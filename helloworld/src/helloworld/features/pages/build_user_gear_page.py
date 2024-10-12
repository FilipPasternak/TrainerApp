import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_switch, create_selection
from helloworld.common.common_page import CommonPage
import csv
import os
import ast


home_gym_equipment = {
    "Weights & Strength Training": [
        "Dumbbells",
        "Kettlebells",
        "Barbell",
        "Weight plates",
        "Medicine ball",
        "Sandbag",
        "Ankle weights"
    ],
    "Resistance & Bodyweight Training": [
        "Resistance bands",
        "TRX suspension trainer",
        "Resistance loop bands",
        "Push-up bars",
        "Parallette bars",
        "Core sliders"
    ],
    "Cardio Equipment": [
        "Treadmill",
        "Stationary bike",
        "Rowing machine",
        "Elliptical machine",
        "Jump rope",
        "Mini stepper",
        "Stepper"
    ],
    "Flexibility & Recovery": [
        "Yoga mat",
        "Foam roller",
        "Exercise ball",
        "Ab wheel",
        "Pull-up bar"
    ],
    "Power & Explosive Training": [
        "Plyo box",
        "Battle ropes"
    ],
    "Benches & Racks": [
        "Adjustable bench",
        "Power rack",
        "Squat rack"
    ]
}

class UserGearPage(CommonPage):
    def __init__(self, main_window, path, next_page='user_goal'):
        super().__init__(path)
        self.main_window = main_window
        self.next_page = next_page
        self.path = path
        self.user_data = None
        self.choosing_box = toga.Box(style=Pack(flex=1))
        self.main_box = toga.Box(style=Pack(direction='column'))
        self.button_box = toga.Box(style=Pack(flex=1))
        self.switches = {}
        self.gear = self.get_items_from_storage()
        for category, items in home_gym_equipment.items():
            self.switches[category] = []

    def startup(self):
        categories = []
        for category, items in home_gym_equipment.items():
            categories.append(category)
            for item in items:
                self.switches[category].append(create_switch(box=self.main_box,
                                                             label=item,
                                                             action=self.toggle_switch,
                                                             style=Pack(padding=5),
                                                             add_to_box=False))
        _ = create_selection(box=self.main_box, options=categories, on_select=self.unroll_category)

        self.main_window.content = self.main_box

    def toggle_switch(self, widget):
        if widget.value:
            if widget.text not in self.gear:
                self.gear.append(widget.text)
        else:
            idx = self.gear.index(widget.text)
            self.gear.pop(idx)

    def unroll_category(self, widget):
        self.main_box.remove(self.choosing_box)
        self.main_box.remove(self.button_box)
        self.choosing_box = toga.Box(style=Pack(flex=1))
        self.button_box = toga.Box(style=Pack(flex=1))

        category = widget.value
        for switch in self.switches[category]:
            if switch.text in self.gear:
                switch.value = True
            self.choosing_box.add(switch)

        self.main_box.add(self.choosing_box)
        create_button(box=self.button_box,
                      action=self.proceed,
                      label='Next',
                      style=Pack(padding=5))
        self.main_box.add(self.button_box)

    def proceed(self, widget):
        self.user_data = [['User_gear'], [self.gear]]
        self.save_user_data_and_proceed(widget=widget)

    def get_items_from_storage(self):
        csv_path = os.path.join(self.path, 'storage', 'user_data.csv')
        with open(csv_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        index = data[0].index('User_gear')
        items = data[1][index]
        items_eval = ast.literal_eval(items)
        return items_eval

