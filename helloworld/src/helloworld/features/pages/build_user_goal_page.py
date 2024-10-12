import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from helloworld.common.create_objects import create_button, create_label, create_switch, create_selection
from helloworld.common.handlers.gpt_handler import GptClient
from helloworld.common.common_page import CommonPage

class UserGoalPage(CommonPage):
    def __init__(self, main_window, path):
        super().__init__(path)
        self.main_window = main_window
        self.path = path
        self.next_page = 'dev_page'
        self.gpt = GptClient(path=path)
        self.user_data = [["Experience", "Goal", "Intensity", "Frequency"], [None, None, None, []]]
        self.days = {'Mon': False,
                     'Tue': False,
                     'Wed': False,
                     'Th': False,
                     'Fri': False,
                     'Sat': False,
                     'Sun': False}

    def startup(self):

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        experience_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_label(box=experience_box,
                     text='Experience:')
        _ = create_selection(box=experience_box,
                             options=['Beginner', 'Worked out before', 'Working out regularly', 'Expert'],
                             on_select=self.on_select_exp)

        goal_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_label(box=goal_box,
                     text='Your goal:')
        _ = create_selection(box=goal_box,
                             options=['Gain muscle', 'Lose weight', 'Healthy lifestyle'],
                             on_select=self.on_select_goal)

        intensity_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_label(box=intensity_box,
                     text='Training intensity:')
        _ = create_selection(box=intensity_box,
                             options=['Relaxing', 'Medium', 'Intense'],
                             on_select=self.on_select_int)

        frequency_box1 = toga.Box(style=Pack(direction=COLUMN, padding=5))
        create_label(box=frequency_box1,
                     text='Training frequency:')
        frequency_box2 = toga.Box(style=Pack(direction=ROW, padding=5))
        for day in ['Mon', 'Tue', 'Wed', 'Th', 'Fri', 'Sat', 'Sun']:
            create_switch(box=frequency_box2, action=self.switch_action, label=day)

        main_box.add(experience_box)
        main_box.add(goal_box)
        main_box.add(intensity_box)
        main_box.add(frequency_box1)
        main_box.add(frequency_box2)
        create_button(box=main_box, action=self.proceed, label='Next')

        self.main_window.content = main_box

    def on_select_exp(self, widget):
        self.user_data[1][0] = widget.value

    def on_select_goal(self, widget):
        self.user_data[1][1] = widget.value

    def on_select_int(self, widget):
        self.user_data[1][2] = widget.value

    def switch_action(self, widget):
        if widget.value:
            self.days[widget.text] = True
        else:
            self.days[widget.text] = False

    def proceed(self, widget):
        for day, value in self.days.items():
            if value:
                print(self.user_data, self.user_data[1], self.user_data[1][3])
                self.user_data[1][3].append(day)
        self.save_user_data_and_proceed(widget=widget)

