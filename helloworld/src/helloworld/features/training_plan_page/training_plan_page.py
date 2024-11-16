import os
from kivy.metrics import dp
from kivy.clock import Clock

from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout

from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.tab import MDTabsBase, MDTabs

from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import popup, Separator


class Tab(MDFloatLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'horizontal'

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



class GeneratePlanPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.plan = self.read_json_file('workout_plan.json')
        self.attempt_count = 0
        self.main_content_container = None

    def on_pre_leave(self, *args):
        self.clear_widgets()

    def on_pre_enter(self, *args):

        top_anchor = MDAnchorLayout(anchor_y='top',
                                    size_hint=[1, .15])
        top_container = MDBoxLayout(orientation='vertical')
        tabs_container = MDTabs()
        tabs_container.bind(on_tab_switch=self.on_tab_switch)

        top_container.add_widget(tabs_container)
        top_anchor.add_widget(top_container)

        center_scrollview = MDScrollView(
            size_hint=(1, .75),
            do_scroll_x=False
        )
        self.main_content_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(5),
            size_hint_y=None,
            pos_hint={'center_x': 0.5})
        self.main_content_container.bind(minimum_height=self.main_content_container.setter('height'))

        bottom_anchor = MDAnchorLayout(anchor_y='bottom',
                                       size_hint=[1, .1])
        bottom_container = MDBoxLayout(orientation='horizontal',
                                       padding=[dp(15), dp(30), dp(15), 0],
                                       spacing=dp(50))
        back_button = MDIconButton(
            icon='arrow-left-bold',
            size_hint=(None, None),
            icon_size=dp(50),
            width=dp(100),
            height=dp(50),
            pos_hint={'center_y': .5},
            on_release=self.go_to_start_page
        )

        start_button = MDIconButton(
            icon='play-circle',
            size_hint=(None, None),
            icon_size=dp(50),
            width=dp(100),
            height=dp(50),
            pos_hint={'center_y': .5, 'center_x': .5},
            on_release=self.go_to_training_assistant_page
        )

        bottom_container.add_widget(back_button)
        bottom_container.add_widget(start_button)
        bottom_anchor.add_widget(bottom_container)

        tabs_list = []
        if self.plan:
            for day, _ in self.plan.items():
                if day != "Date":
                    tab = Tab(title=f'{day}')
                    tabs_list.append(tab)
                    tabs_container.add_widget(tab)

        else:
            info_label = MDLabel(text='No plan generated...',
                                 size_hint_y=None,
                                 height=dp(50))
            new_button = MDRaisedButton(
                text='Generate new training plan!',
                size_hint=(None, None),
                font_size=20,
                width=dp(300),
                height=dp(50),
                pos_hint={'center_x': 0.5, 'center_y': .7},
                on_release=self.generate_plan
            )

            self.main_content_container.add_widget(info_label)
            self.main_content_container.add_widget(new_button)

        main_layout = MDBoxLayout(orientation='vertical', padding=[0, 0, 0, dp(50)])
        center_scrollview.add_widget(self.main_content_container)
        main_layout.add_widget(top_anchor)
        main_layout.add_widget(center_scrollview)
        main_layout.add_widget(bottom_anchor)

        self.add_widget(main_layout)

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        self.main_content_container.clear_widgets()

        label = ""
        category = list(self.plan[tab_text].keys())
        label += ', '.join(category[:2]) if len(category) >= 2 else category[0]
        self.selected_training_day = (tab_text, category)

        self.main_content_container.add_widget(MDLabel(
            text=label,
            size_hint_y=None,
            height=dp(20),
            font_style='H5'
        ))
        for category in self.plan[tab_text]:
            self.main_content_container.add_widget(Separator())
            exercises_list = self.plan[tab_text][category].split(',')
            for exercise in exercises_list:
                ex_button = MDRectangleFlatButton(
                    text=exercise.capitalize(),
                    size_hint=(None, None),
                    font_size=20,
                    width=dp(300),
                    height=dp(50),
                    pos_hint={'center_x': 0.5},
                    on_release=self.go_to_description
                )
                ex_button.custom_data = category
                self.main_content_container.add_widget(ex_button)

    def go_to_description(self, instance):
        category = instance.custom_data
        exercise = instance.text
        details = self.get_exercise_details(category=category, exercise=exercise)

        content = ExerciseDetailsContent(
            details=details
        )

        dialog = MDDialog(
            title=exercise,
            type='custom',
            content_cls=content,
            buttons=[]
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

    def generate_plan(self, instance):
        instance.text = 'Generating, please wait...'
        Clock.schedule_once(lambda dt: self._generate_plan(instance), 0.1)

    def _generate_plan(self, instance):
        self.attempt_count += 1
        try:
            stored_user_data = self.get_items_from_storage()
            self.gpt_client.generate_plan(stored_user_data)
            self.attempt_count = 0
            self.plan = self.read_json_file('workout_plan.json')
            self.on_pre_enter()
        except Exception as e:
            if self.attempt_count < 5:
                Clock.schedule_once(lambda dt: self._generate_plan(instance), 0.5)
            else:
                self.attempt_count = 0
                popup(title='Error', info='Something went wrong, try once again...')
                instance.text = 'Generate your training plan!'

