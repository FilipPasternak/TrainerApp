from helloworld.common.common_page import CommonPage
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class UserDataPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.user_data = None
        self.next_page = 'place_page'

    def proceed(self):
        self.user_data = {'Name': self.ids["name_input"].text,
                          'Sex': self.ids["gender_input"].text,
                          'Age': self.ids["age_input"].text,
                          'Weight': self.ids["weight_input"].text,
                          'Height':  self.ids["height_input"].text}
        passed = True

        for item, val in self.user_data.items():
            if val == '':   # if no input provided then raise error
                passed = False
                self.error_popup(item)
                break
            if item in ['Age', 'Weight', 'Height']:
                try:
                    self.user_data[item] = int(val)
                except ValueError:
                    passed = False
                    self.error_popup(item)
                    break
            if item == 'Sex' and val == 'Select Gender':
                passed = False
                self.error_popup('Gender')
                break

        if passed:
            self.save_user_data_and_proceed()

    @staticmethod
    def error_popup(value):
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
