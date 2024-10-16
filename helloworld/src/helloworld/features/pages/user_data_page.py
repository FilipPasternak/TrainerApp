import toga
from toga.style import Pack
from helloworld.common.create_objects import create_button, create_text_box, create_label
from helloworld.common.common_page import CommonPage


class FirstRunUserDataPage(CommonPage):
    def __init__(self, main_window, path):
        super().__init__(path)
        self.main_window = main_window
        self.user_data = {}
        self.next_page = 'user_place'
        self.path = path
        self.name_input = None
        self.sex_input = None
        self.age_input = None
        self.weight_input = None
        self.height_input = None

    def startup(self):
        main_box = toga.Box(style=Pack(direction='column'))
        create_label(box=main_box,
                     text='Your name',
                     style=Pack(direction='row', padding=5))
        self.name_input = create_text_box(box=main_box,
                                          style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your sex',
                     style=Pack(direction='row', padding=5))
        self.sex_input = create_text_box(box=main_box,
                                         style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your age',
                     style=Pack(direction='row', padding=5))
        self.age_input = create_text_box(box=main_box,
                                         style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your weight',
                     style=Pack(direction='row', padding=5))
        self.weight_input = create_text_box(box=main_box,
                                            style=Pack(direction='row', padding=5))

        create_label(box=main_box,
                     text='Your height',
                     style=Pack(direction='row', padding=5))
        self.height_input = create_text_box(box=main_box,
                                            style=Pack(direction='row', padding=5))

        create_button(box=main_box,
                      action=self.proceed,
                      label='Next',
                      style=Pack(direction='row', padding=5))

        self.main_window.content = main_box
        self.main_window.show()

    def proceed(self, widget):
        self.user_data = {'Name': self.name_input.value,
                          'Sex': self.sex_input.value,
                          'Age': self.age_input.value,
                          'Weight': self.weight_input.value,
                          'Height': self.height_input.value}
        self.save_user_data_and_proceed(widget)
