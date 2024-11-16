from helloworld.common.common_page import CommonPage
from helloworld.common.common_objects import TriangleButton
from kivy.metrics import dp, Metrics
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton


class StartPage(CommonPage):
    def __init__(self, path, **kw):
        super().__init__(path, **kw)
        self.path = path

    def on_pre_enter(self, *args):
        max_height_dp = Window.height / Metrics.density
        max_width_dp = Window.width / Metrics.density

        diet_button = TriangleButton(vertices=[
            dp(0), dp(0),
            dp(max_width_dp) + dp(100), dp(0),
            dp(0), dp(max_height_dp) - dp(100)
        ],
            on_release=self.proceed_diet)
        training_button = TriangleButton(vertices=[
            dp(max_width_dp), dp(max_height_dp),
            -dp(80), dp(max_height_dp),
            dp(max_width_dp), dp(150)
        ], on_release=self.proceed_training)

        settings_button = MDIconButton(
            icon="cog",
            pos_hint={"right": 1, "y": 0.91},
            size_hint=(.1, .1),
        )
        self.ids.main_start_layout.add_widget(diet_button)
        self.ids.main_start_layout.add_widget(training_button)
        self.ids.main_start_layout.add_widget(settings_button)

    def proceed_diet(self):
        self.manager.transition = SlideTransition(direction='right')
        self.go_to_diet_page()

    def proceed_training(self):
        self.manager.transition = SlideTransition(direction='left')
        self.go_to_training_plan_page()
