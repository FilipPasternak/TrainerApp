from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import ToggleButton
from kivy.metrics import dp

class UserPlacePage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.next_page = 'goal_page'
        self.user_data = {}
        self.switches = [
            ToggleButton(
                text='Fully equipped gym',
                size_hint=[None, None],
                width=dp(200),
                height=dp(50),
                pos_hint={'center_x': 0.5},
                group='x'),
            ToggleButton(
                text='Only free weights gym',
                size_hint=[None, None],
                width=dp(200),
                height=dp(50),
                pos_hint={'center_x': 0.5},
                group='x'),
            ToggleButton(
                text='At home with equipment',
                size_hint=[None, None],
                width=dp(200),
                height=dp(50),
                pos_hint={'center_x': 0.5},
                group='x'),
            ToggleButton(
                text='At home without equipment',
                size_hint=[None, None],
                width=dp(200),
                height=dp(50),
                pos_hint={'center_x': 0.5},
                group='x'),
        ]

    def on_pre_enter(self, *args):
        for switch in self.switches:
            self.ids.content_container.add_widget(switch)

    def proceed(self):
        for switch in self.switches:
            if switch.state == 'down':
                self.user_data['Place'] = switch.text

        if self.user_data['Place'] == 'At home with equipment':
            self.next_page = 'gear_page'
        self.save_user_data_and_proceed()

