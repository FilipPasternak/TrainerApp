from helloworld.common.common_page import CommonPage

from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

class DishDetailsContent(MDBoxLayout):
    def __init__(self, instruction, ingredients, nutrients, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        scroll_view = ScrollView(size_hint=(1, None), size=(dp(360), dp(400)))
        content_layout = MDBoxLayout(orientation='vertical', size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        ingredients_label = MDLabel(
            text=f"[b]Ingredients:[/b]\n{ingredients}\n",
            markup=True,
            theme_text_color="Primary",
            size_hint_y=None
        )
        ingredients_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        content_layout.add_widget(ingredients_label)

        instruction_label = MDLabel(
            text=f"[b]Instruction:[/b]\n{instruction}\n",
            markup=True,
            theme_text_color="Primary",
            size_hint_y=None
        )
        instruction_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        content_layout.add_widget(instruction_label)

        nutrients_label = MDLabel(
            text=f"[b]Nutrients:[/b]\n{nutrients}",
            markup=True,
            theme_text_color="Primary",
            size_hint_y=None
        )
        nutrients_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        content_layout.add_widget(nutrients_label)

        scroll_view.add_widget(content_layout)
        self.add_widget(scroll_view)


class DietPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path
        self.diet_dict = None
        self.generate_diet_button = None
        self.go_to_diet_button = None
        self.diet = self.read_json_file('diet.json')
        self.recipes = self.read_json_file('recipes.json')

    def on_pre_leave(self, *args):
        self.ids.diet_layout.clear_widgets()

    def on_pre_enter(self, *args):
        self.generate_diet_button = MDRaisedButton(
            text='Generate new diet plan!',
            size_hint=[None, None],
            height=self.ids.diet_layout.height / 10,
            width=self.ids.diet_layout.width * 0.9,
            on_release=self.generate_diet)
        self.go_to_diet_button = MDRaisedButton(
            text='Go to your diet plan!',
            size_hint=[None, None],
            height=self.ids.diet_layout.height / 10,
            width=self.ids.diet_layout.width * 0.9,
            on_release=self.go_to_diet_days_page)

        self.ids.diet_layout.add_widget(self.generate_diet_button)
        self.ids.diet_layout.add_widget(self.go_to_diet_button)

    def generate_diet(self, instance):
        self.diet_dict = self.gpt_client.generate_diet(self.get_items_from_storage())
        self.go_to_diet_days_page(None)

    def go_to_diet_days_page(self, instance):
        self.ids.diet_layout.remove_widget(self.generate_diet_button)
        self.ids.diet_layout.remove_widget(self.go_to_diet_button)

        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10)
        )

        box_layout = MDBoxLayout(
            padding=[dp(10), dp(20), dp(10), 0],
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None
        )
        box_layout.bind(minimum_height=box_layout.setter('height'))

        for day in self.diet.keys():
            headline = MDLabel(
                text=day.capitalize(),
                halign="center",
                theme_text_color="Primary",
                font_style="H5",
                size_hint_y=None,
                height=dp(50)
            )
            box_layout.add_widget(headline)

            for dish in self.diet[day]:
                button = MDRectangleFlatButton(
                    text=self.truncate_string(dish, max_length=39),
                    pos_hint={'center_x': .5},
                    size_hint=[.9, .1],
                    on_release=self.open_dish_details
                )
                button.dish_name = dish
                box_layout.add_widget(button)

        scroll_view.add_widget(box_layout)
        self.ids.diet_layout.add_widget(scroll_view)

        self.ids.diet_layout.add_widget(MDRaisedButton(
            text='Back',
            size_hint=[.3, .1],
            pos_hint={'center_x': .5},
            on_release=self.go_to_start_page
        ))

    def open_dish_details(self, instance):
        dish_name = instance.dish_name
        details = self.recipes['Recipes'][dish_name]
        instruction = details['Instruction']
        ingredients = details['Ingredients']
        nutrients = details['Nutrients']

        modified_instruction = instruction.replace('. ', '.\n')

        ingredients_str = self.get_string_from_list(ingredients)
        nutrients_str = self.get_string_from_list(nutrients)

        content = DishDetailsContent(
            instruction=modified_instruction,
            ingredients=ingredients_str,
            nutrients=nutrients_str
        )

        dialog = MDDialog(
            title=dish_name,
            type='custom',
            content_cls=content,
            buttons=[]
        )

        dialog.open()

    @staticmethod
    def get_string_from_list(from_list):
        result_str = ''
        for elem in from_list:
            result_str += f'• {elem[0]} - {elem[1]}\n'
        return result_str.strip()

    @staticmethod
    def truncate_string(s, max_length, suffix='...'):
        if len(s) <= max_length:
            return s
        else:
            return s[:max_length - len(suffix)] + suffix
