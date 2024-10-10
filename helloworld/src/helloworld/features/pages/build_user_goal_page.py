import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from helloworld.common.create_objects import create_button, create_label, create_switch, create_selection
from helloworld.common.handlers.gpt_handler import GptClient

class UserGoalPage:
    def __init__(self, main_window, path):
        self.main_window = main_window
        self.path = path
        self.next_page = 'dev_page'
        self.gpt = GptClient(path=path)

    def startup(self):
        import helloworld.common.actions as actions

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        experience_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_label(box=experience_box,
                     text='Experience:')
        _ = create_selection(box=experience_box,
                             options=['Beginner', 'Worked out before', 'Working out regularly', 'Expert'],
                             on_select=self.on_select)

        goal_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_label(box=goal_box,
                     text='Your goal:')
        _ = create_selection(box=goal_box,
                             options=['Gain muscle', 'Lose weight', 'Healthy lifestyle'],
                             on_select=self.on_select)

        intensity_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_label(box=intensity_box,
                     text='Training intensity:')
        _ = create_selection(box=intensity_box,
                             options=['Relaxing', 'Medium', 'Intense'],
                             on_select=self.on_select)

        frequency_box1 = toga.Box(style=Pack(direction=COLUMN, padding=5))
        create_label(box=frequency_box1,
                     text='Training frequency:')
        frequency_box2 = toga.Box(style=Pack(direction=ROW, padding=5))
        for day in ['Mon', 'Tue', 'Wed', 'Th', 'Fri', 'Sat', 'Sun']:
            create_button(box=frequency_box2, action=self.button_push, label=day)

        main_box.add(experience_box)
        main_box.add(goal_box)
        main_box.add(intensity_box)
        main_box.add(frequency_box1)
        main_box.add(frequency_box2)
        self.main_window.content = main_box

    def on_select(self):
        pass

    def button_push(self):
        pass
