from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import ToggleButton

from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.label import MDLabel

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
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.gear = []
        self.user_data = {}
        self.next_page = 'goal_page'
        self.toggle_buttons = []

    def on_enter(self):
        switches_layout = self.ids.Switches

        switches_layout.clear_widgets()

        for category, equipment_list in home_gym_equipment.items():
            category_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
            category_layout.bind(minimum_height=category_layout.setter('height'))

            category_label = MDLabel(text=category, size_hint_y=None, height=30)
            category_layout.add_widget(category_label)

            for equipment in equipment_list:
                toggle_button = ToggleButton(text=equipment, size_hint_y=None, height=50)
                self.toggle_buttons.append(toggle_button)
                category_layout.add_widget(toggle_button)

            switches_layout.add_widget(category_layout)

    def proceed(self):
        for button in self.toggle_buttons:
            if button.state == 'down':
                self.gear.append(button.text)

        self.user_data['User_gear'] = self.gear
        self.save_user_data_and_proceed()


