import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_text_box, create_label
from helloworld.features.sections.first_run_section import FirstRunSection

class FirstRunUserDataPage(FirstRunSection):
    def __init__(self, main_window, path):
        super().__init__(path)
        self.main_window = main_window
        self.user_data = None
        self.next_page = 'user_place'
        self.path = path

    def startup(self):
        main_box = toga.Box(style=Pack(direction='column'))
        create_label(box=main_box,
                     text='Your name',
                     style=Pack(direction='row', padding=5))
        name_input = create_text_box(box=main_box,
                                     style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your sex',
                     style=Pack(direction='row', padding=5))
        sex_input = create_text_box(box=main_box,
                                    style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your age',
                     style=Pack(direction='row', padding=5))
        age_input = create_text_box(box=main_box,
                                    style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your weight',
                     style=Pack(direction='row', padding=5))
        weight_input = create_text_box(box=main_box,
                                       style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your height',
                     style=Pack(direction='row', padding=5))
        height_input = create_text_box(box=main_box,
                                       style=Pack(direction='row', padding=5))

        self.user_data = [['Name', 'Sex', 'age', 'Weight', 'Height', 'User_gear'],
                          [name_input, sex_input, age_input, weight_input, height_input, '[]']]

        create_button(box=main_box,
                      action=self.save_user_data_and_proceed,
                      label='Next',
                      style=Pack(direction='row', padding=5))

        self.main_window.content = main_box
        self.main_window.show()




