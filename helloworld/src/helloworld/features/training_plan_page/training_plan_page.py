import time

from helloworld.common.common_page import CommonPage
import os
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from helloworld.resources.gradient import Gradient
from kivy.clock import Clock


#GLOBAL
plan = None

class GeneratePlanPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.plan = None

    def on_pre_enter(self, *args):
        main_layout = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])
        gradient = Gradient()
        self.add_widget(gradient)

        top_anchor = AnchorLayout(anchor_y='center')
        top_button = Button(
            text='Generate your training plan!',
            size_hint=(None, None),
            font_size=20,
            width=dp(300),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.generate_plan
        )
        top_anchor.add_widget(top_button)
        main_layout.add_widget(top_anchor)

        bottom_anchor = AnchorLayout(anchor_y='bottom')
        back_button = Button(
            text='Back',
            size_hint=(None, None),
            font_size=20,
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_start_page
        )
        bottom_anchor.add_widget(back_button)
        main_layout.add_widget(bottom_anchor)

        self.add_widget(main_layout)

    def generate_plan(self, instance):
        instance.text = 'Generating, please wait...'
        Clock.schedule_once(lambda dt: self._generate_plan(instance), 0.1)

    def _generate_plan(self, instance):
        stored_user_data = self.get_items_from_storage()
        plan = self.gpt_client.generate_plan(stored_user_data)
        self.go_to_exercises()

    def go_to_exercises(self):
        self.manager.current = 'exercises'

class ExercisesPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.plan = self.read_json_file('workout_plan.json')
        self.exercises_page = None
        self.description_page = None
        self.exercises_container = None

    def on_pre_enter(self, *args):
        main_layout = PageLayout()

        day_page = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])
        self.exercises_page = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])
        self.description_page = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])

        # DAY PAGE START ------------------------------------------
        day_top_anchor = AnchorLayout(anchor_y='top')
        days_container = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])
        for day, exercises in self.plan.items():
            label = f"{day}: "
            category = list(exercises.keys())
            label += ', '.join(category[:2]) if len(category) == 2 else category[0]
            top_button = ToggleButton(
                text=label,
                size_hint=(None, None),
                font_size=20,
                width=dp(300),
                height=dp(50),
                pos_hint={'center_x': 0.5},
                on_release=self.load_exercises
            )
            days_container.add_widget(top_button)
        day_top_anchor.add_widget(days_container)
        day_page.add_widget(day_top_anchor)

        day_bottom_anchor = AnchorLayout(anchor_y='bottom')
        back_button = Button(
            text='Back',
            size_hint=(None, None),
            font_size=20,
            width=dp(200),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_start_page
        )
        day_bottom_anchor.add_widget(back_button)
        day_page.add_widget(day_bottom_anchor)
        # DAY PAGE END --------------------------------------------

        # EXERCISES PAGE START ------------------------------------
        exercises_top_anchor = AnchorLayout(anchor_y='top')
        self.exercises_container = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])

        # day = self.get_day_name_from_label()
        # categories = list(self.plan[day].keys())
        # exercises = list(self.plan[day].values())
        #
        # for i in range(len(categories)):
        #     create_label(box=new_main_box,
        #                  text=categories[i])
        #     exercises_list = exercises[i].split(',')
        #     for exercise in exercises_list:
        #         create_button(box=new_main_box,
        #                       label=exercise.capitalize(),
        #                       custom_data=categories[i],
        #                       action=self.go_to_description)
        #
        # create_button(box=new_main_box,
        #               label='Back',
        #               action=self.go_back_to_calendar,
        #               style=Pack(padding=15, alignment='center'))
        # self.exercises_window = new_main_box
        # self.main_window.content = new_main_box
        # EXERCISES PAGE END ------------------------------------

        main_layout.add_widget(day_page)
        self.add_widget(main_layout)


    def load_exercises(self, instance):
        pass


class TrainingPlanPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
    #     main_box = toga.Box(style=Pack(direction='column'))
    #
    #     self.top_label = toga.Label('Generate your training plan!', style=Pack(padding=10))
    #     main_box.add(self.top_label)
    #
    #     create_button(box=main_box,
    #                   action=self.generate_plan,
    #                   label='Generate',
    #                   style=Pack(padding=5))
    #
    #     create_button(box=main_box,
    #                   label='Back',
    #                   action=self.go_to_next_page(page='dev_page'),
    #                   style=Pack(padding=15, alignment='center'))
    #
    #     self.main_window.content = main_box
    #

    #

    #
    # def go_to_exercises(self, widget):

    #
    # @staticmethod
    # def get_day_name_from_label(widget):
    #     label_split = widget.text.split(':')
    #     return label_split[0]
    #
    # def go_to_description(self, widget):
    #     new_main_box = toga.Box(style=Pack(direction=COLUMN))
    #     category = widget.custom_data
    #     exercise = widget.text
    #     details = self.get_exercise_details(category, exercise)
    #     for item, value in details.items():
    #         create_label(box=new_main_box,
    #                      text=f"{item}: \n{self.insert_newlines(text=value, max_width=500)}",
    #                      style=Pack(width=500, alignment="left", font_size=12, padding=10))
    #
    #     create_button(box=new_main_box,
    #                   label='Back',
    #                   action=self.go_back_to_exercises,
    #                   style=Pack(padding=15, alignment='center'))
    #
    #     self.main_window.content = new_main_box
    #
    # def get_exercise_details(self, category, exercise):
    #     place = self.get_items_from_storage(item='Place')
    #     json_files = {
    #         'Fully equipped gym': os.path.join('exercises', 'full_gym_ex.json'),
    #         'Only free weights gym': os.path.join('exercises', 'weights_gym_ex.json'),
    #         'At home with equipment': os.path.join('exercises', 'home_equip_ex.json'),
    #         'At home without equipment': os.path.join('exercises', 'home_no_equip_ex.json')
    #     }
    #     descriptions = self.read_json_file(filename=json_files[place])
    #     if exercise in descriptions[place][category]:
    #         return descriptions[place][category][exercise]
    #     else:
    #         details = self.gpt_client.generate_exercise_details(exercise,
    #                                                             equipment=self.get_items_from_storage(item='User_gear'))
    #         self.add_new_exercise(exercise, category, details, place)
    #         return details
    #
    #
    # def go_back_to_calendar(self, widget):
    #     self.load_plan(widget)
    #
    # def go_back_to_exercises(self, widget):
    #     self.main_window.content = self.exercises_window
