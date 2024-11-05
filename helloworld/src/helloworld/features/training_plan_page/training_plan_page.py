import os
from kivy.metrics import dp
from kivy.clock import Clock

from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.carousel import MDCarousel
from kivy.graphics import Color, Rectangle
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView

from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import popup, Separator


class GeneratePlanPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.plan = None
        self.attempt_count = 0

    def on_pre_enter(self, *args):
        main_layout = MDBoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])

        top_anchor = MDAnchorLayout(anchor_y='center')
        main_content_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            pos_hint={'center_x': 0.5})

        new_button = MDRaisedButton(
            text='Generate new training plan!',
            size_hint=(None, None),
            font_size=20,
            width=dp(300),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': .7},
            on_release=self.generate_plan
        )
        old_button = MDRaisedButton(
            text='Go to your training plan',
            size_hint=(None, None),
            font_size=20,
            width=dp(300),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': .6},
            on_release=self.go_to_exercises
        )

        main_content_container.add_widget(new_button)
        main_content_container.add_widget(old_button)
        top_anchor.add_widget(main_content_container)
        main_layout.add_widget(top_anchor)

        bottom_anchor = MDAnchorLayout(anchor_y='bottom')
        back_button = MDRectangleFlatButton(
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
        self.attempt_count += 1
        try:
            stored_user_data = self.get_items_from_storage()
            self.gpt_client.generate_plan(stored_user_data)
            self.attempt_count = 0
            self.go_to_exercises(instance)
        except Exception as e:
            if self.attempt_count < 5:
                Clock.schedule_once(lambda dt: self._generate_plan(instance), 0.5)
            else:
                self.attempt_count = 0
                popup(title='Error', info='Something went wrong, try once again...')
                instance.text = 'Generate your training plan!'

    def go_to_exercises(self, instance):
        self.manager.current = 'exercises'

class ExercisesPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.plan = self.read_json_file('workout_plan.json')
        self.exercises_page = None
        self.description_page = None
        self.exercises_container = None
        self.main_layout = None

    def on_pre_enter(self, *args):
        self.main_layout = MDCarousel(direction='right')

        day_page = MDBoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])
        self.exercises_page = MDBoxLayout(orientation='vertical')
        self.description_page = MDBoxLayout(orientation='vertical', padding=[dp(10), dp(20), 0, dp(50)])

        # DAY PAGE START ------------------------------------------
        day_top_anchor = MDAnchorLayout(anchor_y='top')
        days_container = MDBoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)], spacing=dp(10))
        for day, exercises in self.plan.items():
            label = f"{day}: "
            category = list(exercises.keys())
            label += ', '.join(category[:2]) if len(category) >= 2 else category[0]
            top_button = MDRaisedButton(
                text=label,
                size_hint=(None, None),
                font_size=20,
                width=dp(300),
                height=dp(50),
                pos_hint={'center_x': 0.5},
                on_press=self.load_exercises
            )
            days_container.add_widget(top_button)
        day_top_anchor.add_widget(days_container)
        day_page.add_widget(day_top_anchor)

        day_bottom_anchor = MDAnchorLayout(anchor_y='bottom')
        back_button = MDFlatButton(
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
        exercises_top_anchor = MDAnchorLayout(anchor_y='top')

        with exercises_top_anchor.canvas.before:
            Color(rgba=(0.9, 0.95, 1, 1))
            exercises_top_anchor.rect = Rectangle(pos=exercises_top_anchor.pos, size=exercises_top_anchor.size)

        exercises_top_anchor.bind(pos=self.update_rect, size=self.update_rect)
        self.exercises_container = MDAnchorLayout(anchor_y='top')

        exercises_top_anchor.add_widget(self.exercises_container)
        self.exercises_page.add_widget(exercises_top_anchor)
        # EXERCISES PAGE END ------------------------------------

        # DESCRIPTION PAGE START --------------------------------


        # DESCRIPTION PAGE END ----------------------------------

        self.main_layout.add_widget(day_page)
        self.main_layout.add_widget(self.exercises_page)
        self.main_layout.add_widget(self.description_page)

        self.add_widget(self.main_layout)

    def load_exercises(self, instance):
        self.exercises_container.clear_widgets()
        self.main_layout.load_next()

        scroll_view = MDScrollView()
        ex_box_layout = MDBoxLayout(orientation='vertical',
                                    padding=[dp(5), dp(20), 0, dp(50)],
                                    spacing=dp(15),
                                    adaptive_height=True)

        day = self.get_day_name_from_label(instance)
        categories = list(self.plan[day].keys())
        exercises = list(self.plan[day].values())

        for i in range(len(categories)):
            ex_box_layout.add_widget(Separator())     # <-------
            ex_box_layout.add_widget(MDLabel(text=categories[i],
                                             pos_hint={'center_x': .5},
                                             height=dp(30),
                                             width=dp(100)))
            exercises_list = exercises[i].split(',')
            for exercise in exercises_list:
                ex_button = MDRectangleFlatButton(
                    text=exercise.capitalize(),
                    size_hint=(None, None),
                    font_size=20,
                    width=dp(300),
                    height=dp(50),
                    pos_hint={'center_x': 0.5, 'center_y': .7},
                    on_release=self.go_to_description
                )
                ex_button.custom_data = categories[i]
                ex_box_layout.add_widget(ex_button)

        scroll_view.add_widget(ex_box_layout)
        self.exercises_container.add_widget(scroll_view)

    def go_to_description(self, widget):
        self.description_page.clear_widgets()
        new_main_box = self.description_page
        category = widget.custom_data
        exercise = widget.text
        details = self.get_exercise_details(category, exercise)
        for item, value in details.items():
            new_main_box.add_widget(MDLabel(
                text=f"{item}: \n{value}"
            ))
        self.main_layout.load_next()

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


    @staticmethod
    def get_day_name_from_label(widget):
        label_split = widget.text.split(':')
        return label_split[0]

    def update_rect(self, instance, *args):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class TrainingPlanPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path


    # EXERCISES PAGE START ------------------------------------
    # exercises_top_anchor = AnchorLayout(anchor_y='top')
    # self.exercises_container = BoxLayout(orientation='vertical', padding=[0, dp(20), 0, dp(50)])

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


    #
    # def go_back_to_calendar(self, widget):
    #     self.load_plan(widget)
    #
    # def go_back_to_exercises(self, widget):
    #     self.main_window.content = self.exercises_window
