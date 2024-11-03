from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import popup, dropdown


class UserDataPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.user_data = None
        self.next_page = 'place_page'

        menu_items = ["Male", "Female"]

        self.gender_menu = dropdown(caller=self.ids.gender_input, items_list=menu_items)

    def proceed(self):
        self.user_data = {'Name': self.ids.name_input.text,
                          'Sex': self.ids.gender_input.text,
                          'Age': self.ids.age_input.text,
                          'Weight': self.ids.weight_input.text,
                          'Height':  self.ids.height_input.text}
        passed = True

        for item, val in self.user_data.items():
            if val == '':   # if no input provided then raise error
                passed = False
                popup(title='Error', info=f"Invalid value: {item}")
                break
            if item in ['Age', 'Weight', 'Height']:
                try:
                    self.user_data[item] = int(val)
                except ValueError:
                    passed = False
                    popup(title='Error', info=f"Invalid value: {item}")
                    break
            if item == 'Sex' and val == 'Select Gender':
                passed = False
                popup(title='Error', info="Invalid value: Gender")
                break

        if passed:
            self.save_user_data_and_proceed()
