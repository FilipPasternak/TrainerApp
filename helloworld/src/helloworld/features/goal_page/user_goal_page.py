from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import popup, ToggleButton, dropdown
from kivy.metrics import dp


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
        self.exp = None
        self.goal = None
        self.intensity = None
        self.toggle_buttons = []
        self.next_page = 'start_page'

    def on_enter(self, *args):
        self.exp = dropdown(caller=self.ids.exp,
                            items_list=['Beginner', 'Worked out before', 'Working out regularly', 'Expert'])
        self.goal = dropdown(caller=self.ids.goal,
                             items_list=['Gain muscle', 'Lose weight', 'Healthy lifestyle'])
        self.intensity = dropdown(caller=self.ids.intensity,
                                  items_list=['Relaxing', 'Medium', 'Intense'])
        layout = self.ids.grid
        for day in self.days.keys():
            button = ToggleButton(
                text=day,
                size_hint=(None, None),
                width=dp(70),
                height=dp(50)
            )
            self.toggle_buttons.append(button)
            layout.add_widget(button)


    def proceed(self):
        self.passed = True
        for button in self.toggle_buttons:
            if button.state == 'down':
                self.days[button.text] = True
        self.user_data['Frequency'] = [day for day, val in self.days.items() if val]

        if any([not self.user_data['Frequency'],
                self.ids.goal.text == 'Your goal',
                self.ids.intensity.text == 'Training intensity',
                self.ids.exp.text == 'Your experience']):
            self.passed = False

        self.user_data['Goal'] = self.ids.goal.text if self.ids.goal.text != 'Your goal' else popup(title='Error', info=f'Please select: {self.ids.goal.text}')
        self.user_data['Intensity'] = self.ids.intensity.text if self.ids.intensity.text != 'Training intensity' else popup(title='Error', info=f'Please select: {self.ids.intensity.text}')
        self.user_data['Experience'] = self.ids.exp.text if self.ids.exp.text != 'Your experience' else popup(title='Error', info=f'Please select: {self.ids.exp.text}')
        if not self.user_data['Frequency']:
            popup(title='Error', info='Select days for your schedule')

        if self.passed:
            self.save_user_data_and_proceed()




