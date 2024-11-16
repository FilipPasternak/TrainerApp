from datetime import datetime
from helloworld.common.common_page import CommonPage
from kivy.clock import Clock
from kivy.uix.label import Label
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp

import os

class EditRepsContent(MDBoxLayout):
    def __init__(self, reps, series, weight, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = [0, dp(10), 0, 0]
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.adaptive_height = True

        content_layout = MDBoxLayout(orientation='vertical',
                                     adaptive_height=True,
                                     spacing=dp(10))
        content_layout.bind(minimum_height=content_layout.setter('height'))

        reps_label = MDLabel(
            text="Reps",
            halign="center",
            font_style="H6"
        )
        self.reps_input = MDTextField(
            hint_text="Enter number of reps",
            text=str(reps),
            size_hint=(1, None),
            height=dp(50),
        )
        content_layout.add_widget(reps_label)
        content_layout.add_widget(self.reps_input)

        series_label = MDLabel(
            text="Series",
            halign="center",
            font_style="H6"
        )
        self.series_input = MDTextField(
            hint_text="Enter number of series",
            text=str(series),
            size_hint=(1, None),
            height=dp(50),
        )
        content_layout.add_widget(series_label)
        content_layout.add_widget(self.series_input)

        weight_label = MDLabel(
            text="Weight (kg)",
            halign="center",
            font_style="H6"
        )
        self.weight_input = MDTextField(
            hint_text="Enter weight (kg)",
            text=str(weight),
            size_hint=(1, None),
            height=dp(50),
        )
        if weight == 'None':
            self.weight_input.disabled = True

        content_layout.add_widget(weight_label)
        content_layout.add_widget(self.weight_input)

        self.add_widget(content_layout)

class ExerciseDetailsContent(MDBoxLayout):
    def __init__(self, details, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        scroll_view = MDScrollView(size_hint=(1, None), size=(dp(360), dp(400)))
        content_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(400))
        content_layout.bind(minimum_height=content_layout.setter('height'))

        label_text = ''
        for item, value in details.items():
            label_text += f"{item}: \n{value}\n\n"

        label = MDLabel(
            text=label_text,
            size_hint_y=None,
            text_size=(dp(300), None),
            valign="top"
        )
        label.bind(texture_size=label.setter('size'))

        content_layout.add_widget(label)

        scroll_view.add_widget(content_layout)
        self.add_widget(scroll_view)


class AssistantPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.plan = self.read_json_file('workout_plan.json')
        self.training = None

        # Timer variables
        self.timer_duration = 10
        self.remaining_time = self.timer_duration
        self.timer_label = None
        self.timer_event = None

        self.current_exercise_idx = 0
        self.current_exercise_name = None
        self.training_listed = []
        self.series = 0
        self.series_current = 0
        self.weight = None
        self.reps = None
        self.last_exercise = ''
        self.day = None
        self.category = None
        self.reps_label = None
        self.dialog = None
        self.training_file_data = None


    def on_pre_enter(self, *args):
        self.day, self.category = self.manager.children[1].selected_training_day

        for workout_name, exercises_str in self.plan[self.day].items():
            exercises_list = [exercise.strip() for exercise in exercises_str.split(',')]
            for exercise in exercises_list:
                self.check_descriptions(workout_name, exercise)

        descriptions = {}
        for cat in self.category:
            cat_descr = self.get_descriptions(cat)
            for key, val in cat_descr.items():
                descriptions[key] = val

        self.training_file_data = self.read_json_file('training_mode.json')

        if not self.check_last_training_date(self.training_file_data['Date'], self.plan["Date"]):
            self.training_file_data = {
                "Mon": None,
                "Tue": None,
                "Wed": None,
                "Th": None,
                "Fri": None,
                "Sat": None,
                "Sun": None,
                "Date": datetime.today().strftime('%Y-%m-%d')
            }
            self.replace_json_file_data('training_mode.json', self.training_file_data)

        if not self.training_file_data[self.day]:
            self.training = self.gpt_client.generate_training(self.plan, self.day, descriptions)
            self.training_file_data[self.day] = self.training
            self.training_file_data['Date'] = datetime.today().strftime('%Y-%m-%d')
            self.replace_json_file_data('training_mode.json', self.training_file_data)
        else:
            self.training = self.training_file_data[self.day]

        self.update_elements()

    def update_elements(self, *args):
        self.training_listed = []
        for key, value in self.training.items():
            self.training_listed.append({key: value})
        for key, value in self.training_listed[self.current_exercise_idx].items():
            self.current_exercise_name = key

        self.timer_duration = int(self.training_listed[self.current_exercise_idx][self.current_exercise_name]["Series time"].strip('s'))
        self.remaining_time = self.timer_duration
        self.series = int(self.training_listed[self.current_exercise_idx][self.current_exercise_name]["Series"])
        self.weight = self.training_listed[self.current_exercise_idx][self.current_exercise_name]["Weight"]
        self.reps = self.training_listed[self.current_exercise_idx][self.current_exercise_name]["Reps"]
        self.build_ui()

    def build_ui(self):
        center_box = self.ids.center_box
        center_box.clear_widgets()

        layout = RelativeLayout()

        if self.current_exercise_name != 'Rest':
            info_button = MDIconButton(
                icon='information',
                pos_hint={'right': 0.98, 'top': 0.98},
                on_release=self.go_to_description
            )
            info_button.exercise = self.current_exercise_name
            layout.add_widget(info_button)

            edit_button = MDIconButton(
                icon='circle-edit-outline',
                pos_hint={'center_x': 0.9, 'center_y': 0.3},
                on_release=self.edit_reps
            )
            layout.add_widget(edit_button)

        self.timer_label = Label(
            text=str(self.remaining_time),
            font_size='64sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        layout.add_widget(self.timer_label)

        bottom_label = Label(
            text=self.current_exercise_name,
            size_hint=(1, None),
            height=dp(70),
            font_size='32sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            halign='center',
            valign='middle'
        )

        series_label = Label(
            text=str(self.series_current) + '/' + str(self.series) if self.current_exercise_name != 'Rest' else '',
            size_hint=(1, .2),
            height=dp(70),
            font_size='32sp',
            pos_hint={'center_x': 0.15, 'center_y': 0.9},
            halign='center',
            valign='middle'
        )

        self.reps_label = Label(
            size_hint=(1, .2),
            height=dp(70),
            font_size='28sp',
            pos_hint={'center_x': 0.4, 'center_y': 0.3},
            halign='center',
            valign='middle'
        )
        if self.current_exercise_name == 'Rest':
            self.reps_label.text = ''
        else:
            if self.weight == 'None':
                self.reps_label.text = 'Reps: ' + self.reps
            else:
                if 's' in self.reps:
                    self.reps_label.text = 'Duration: ' + self.reps
                else:
                    self.reps_label.text = 'Reps: ' + self.reps + 'x' + self.weight

        series_label.bind(size=self.update_text_size)
        bottom_label.bind(size=self.update_text_size)
        self.reps_label.bind(size=self.update_text_size)
        layout.add_widget(self.reps_label)
        layout.add_widget(series_label)
        layout.add_widget(bottom_label)

        center_box.add_widget(layout)

        if self.current_exercise_name == 'Rest':
            self.start_training()
        else:
            self.pause_training()

    def update_text_size(self, instance, value):
        instance.text_size = instance.size

    def toggle_training(self, *args):
        if self.timer_event:
            self.pause_training()
        else:
            self.start_training()

    def start_training(self):
        self.ids.start_stop.icon = 'pause-circle'
        self.start_timer()

    def pause_training(self):
        self.ids.start_stop.icon = 'play-circle'
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None

    def start_timer(self):
        if not self.timer_event:
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.remaining_time -= 1
        if self.remaining_time >= 0:
            self.timer_label.text = str(self.remaining_time) + 's'
        else:
            self.pause_training()

    def next(self, *args):
        self.pause_training()
        self.remaining_time = self.timer_duration
        self.timer_label.text = str(self.remaining_time)
        self.last_exercise = self.current_exercise_name

        if self.current_exercise_name == 'Rest':
            for key, value in self.training_listed[self.current_exercise_idx].items():
                self.current_exercise_name = key
            self.update_elements()

        if self.training_listed[self.current_exercise_idx] == self.training_listed[-1]:
            self.go_to_training_plan_page()
        else:
            if self.last_exercise != 'Rest':
                self.series_current += 1
            if self.series <= self.series_current:
                self.series_current = 0
                self.current_exercise_idx += 1
                self.update_elements()
            self.rest()
            if self.last_exercise == 'Rest':
                self.update_elements()

    def rest(self):
        self.timer_duration = int(self.training_listed[self.current_exercise_idx][self.current_exercise_name]["Rest"].strip('s'))
        self.remaining_time = self.timer_duration
        self.current_exercise_name = 'Rest'
        self.series = 1
        self.build_ui()

    def get_descriptions(self, category):
        place = self.get_items_from_storage(item='Place')
        json_files = {
            'Fully equipped gym': os.path.join('exercises', 'full_gym_ex.json'),
            'Only free weights gym': os.path.join('exercises', 'weights_gym_ex.json'),
            'At home with equipment': os.path.join('exercises', 'home_equip_ex.json'),
            'At home without equipment': os.path.join('exercises', 'home_no_equip_ex.json')
        }
        descriptions = self.read_json_file(filename=json_files[place])
        return descriptions[place][category]

    def check_descriptions(self, category, exercise):
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
            details = self.gpt_client.generate_exercise_details(
                exercise,
                equipment=self.get_items_from_storage(item='User_gear')
            )
            self.add_new_exercise(exercise, category, details, place)
            return details

    def go_to_description(self, instance):
        exercise = instance.exercise
        category = None
        for cat in self.category:
            if exercise in self.plan[self.day][cat].split(','):
                category = cat

        details = self.get_exercise_details(category=category, exercise=exercise)

        content = ExerciseDetailsContent(
            details=details
        )

        dialog = MDDialog(
            title=exercise,
            type='custom',
            content_cls=content,
            buttons=[],
            auto_dismiss=True
        )

        dialog.open()

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
            print(exercise)
            return details

    def edit_reps(self, *args):
        content = EditRepsContent(
            reps=self.reps,
            series=self.series,
            weight=self.weight
        )


        save_button = MDFlatButton(
            text='SAVE',
            on_release=self.save_edited_reps
        )

        self.dialog = MDDialog(
            title='Edit exercise',
            type='custom',
            content_cls=content,
            buttons=[save_button],
            auto_dismiss=False
        )

        self.dialog.open()

    def save_edited_reps(self, *args):
        content = self.dialog.content_cls

        self.training_file_data[self.day][self.current_exercise_name]["Reps"] = str(content.reps_input.text)
        self.training_file_data[self.day][self.current_exercise_name]["Series"] = str(content.series_input.text)
        self.training_file_data[self.day][self.current_exercise_name]["Weight"] = str(content.weight_input.text)
        self.replace_json_file_data('training_mode.json', self.training_file_data)

        self.training = self.training_file_data[self.day]
        self.update_elements()

        self.dialog.dismiss()

    @staticmethod
    def check_last_training_date(date1_str, date2_str):
        date1 = datetime.strptime(date1_str, '%Y-%m-%d').date()
        date2 = datetime.strptime(date2_str, '%Y-%m-%d').date()

        iso_year1, iso_week1, _ = date1.isocalendar()
        iso_year2, iso_week2, _ = date2.isocalendar()

        return iso_year1 == iso_year2 and iso_week1 == iso_week2
