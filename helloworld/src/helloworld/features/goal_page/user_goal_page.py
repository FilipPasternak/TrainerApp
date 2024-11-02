from helloworld.common.common_page import CommonPage
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class UserGoalPage(CommonPage):
    def __init__(self, path='', **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.user_data = {}
        self.days = {'Mon': False,
                     'Tue': False,
                     'Wed': False,
                     'Th': False,
                     'Fri': False,
                     'Sat': False,
                     'Sun': False}
        self.passed = True
        self.next_page = 'start_page'

    def on_enter(self, *args):
        layout = self.ids.grid

        for day in self.days.keys():
            button = ToggleButton(
                text=day,
                size_hint=(None, None),
                width=dp(70),
                height=dp(50)
            )
            button.bind(state=self.toggle)
            layout.add_widget(button)

    def toggle(self, instance, state):
        if state == 'down':
            self.days[instance.text] = True
        else:
            self.days[instance.text] = False

    def proceed(self):
        self.passed = True
        self.user_data['Frequency'] = [day for day, val in self.days.items() if val]
        self.user_data['Goal'] = self.ids.goal.text if self.ids.goal.text != 'Your goal' else self.error_popup(self.ids.goal.text)
        self.user_data['Intensity'] = self.ids.intensity.text if self.ids.intensity.text != 'Training intensity' else self.error_popup(self.ids.intensity.text)
        self.user_data['Experience'] = self.ids.exp.text if self.ids.exp.text != 'Your experience' else self.error_popup(self.ids.exp.text)
        if not self.user_data['Frequency']:
            self.error_popup('Select days for your schedule')

        if self.passed:
            self.save_user_data_and_proceed()

    def error_popup(self, value):
        self.passed = False
        box = BoxLayout(orientation='vertical')
        error_message = Label(text=f'Invalid value: {value}')
        close_button = Button(text='Close', size_hint=(1, 0.3))
        box.add_widget(error_message)
        box.add_widget(close_button)

        popup = Popup(
            title="Error",
            content=box,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        close_button.bind(on_release=popup.dismiss)

        popup.open()
