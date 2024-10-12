import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_label, create_switch
from toga.style.pack import COLUMN
from helloworld.common.common_page import CommonPage

class FirstRunUserPlacePage(CommonPage):
    def __init__(self, main_window, path):
        self.path = path
        self.main_window = main_window
        self.full_gym_switch = None
        self.small_gym_switch = None
        self.equipped_home_switch = None
        self.no_gear_home_switch = None
        self.next_page = None
        self.user_data = None

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        create_label(box=main_box, text='Pick your training place', style=Pack(padding=5))

        self.full_gym_switch = create_switch(box=main_box,
                                             label='Fully equipped gym',
                                             action=self.toggle_switch,
                                             style=Pack(padding=5))
        self.small_gym_switch = create_switch(box=main_box,
                                              label='Only free weights gym',
                                              action=self.toggle_switch,
                                              style=Pack(padding=5))
        self.equipped_home_switch = create_switch(box=main_box,
                                                  label='At home with equipment',
                                                  action=self.toggle_switch,
                                                  style=Pack(padding=5))
        self.no_gear_home_switch = create_switch(box=main_box,
                                                 label='At home without equipment',
                                                 action=self.toggle_switch,
                                                 style=Pack(padding=5))

        create_button(box=main_box,
                      action=self.proceed,
                      label='Next',
                      style=Pack(padding=5))

        self.main_window.content = main_box
        self.main_window.show()

    def toggle_switch(self, widget):
        switches = [self.full_gym_switch, self.small_gym_switch, self.equipped_home_switch, self.no_gear_home_switch]
        for switch in switches:
            if widget.value:
                if widget == switch:
                    pass
                else:
                    switch.value = False
                    switch.enabled = False
            else:
                if widget == switch:
                    pass
                else:
                    switch.value = False
                    switch.enabled = True

    def proceed(self, widget):
        data = ''
        if self.equipped_home_switch.value:
            data = 'At home with equipment'
            self.next_page = 'user_gear'
        elif self.full_gym_switch.value:
            data = 'Fully equipped gym'
            self.next_page = 'user_goal'
        elif self.small_gym_switch.value:
            data = 'Only free weights gym'
            self.next_page = 'user_goal'
        elif self.no_gear_home_switch.value:
            data = 'At home without equipment'
            self.next_page = 'user_goal'

        self.user_data = [['Place'], [data]]
        self.save_user_data_and_proceed(widget)

