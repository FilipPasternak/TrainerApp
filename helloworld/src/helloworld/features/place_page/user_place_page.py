from helloworld.common.common_page import CommonPage

class UserPlacePage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.next_page = 'goal_page'
        self.user_data = {}
        self.last_pressed_switch = None


    def toggle_switch(self, text):
        self.user_data['Place'] = text
        if self.last_pressed_switch:
            self.last_pressed_switch.state = 'normal'
        self.last_pressed_switch = self.ids[text]

    def proceed(self):
        if self.user_data['Place'] == 'At home with equipment':
            self.next_page = 'gear_page'
        self.save_user_data_and_proceed()

