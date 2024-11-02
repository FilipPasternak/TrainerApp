
from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
import os
from helloworld.features.dev_page.dev_page import DevPage
from helloworld.features.diet_page.diet_page import DietPage
from helloworld.features.data_page.user_data_page import UserDataPage
from helloworld.features.place_page.user_place_page import UserPlacePage
from helloworld.features.gear_page.user_gear_page import UserGearPage
from helloworld.features.goal_page.user_goal_page import UserGoalPage
from helloworld.features.training_plan_page.training_plan_page import GeneratePlanPage, ExercisesPage
from helloworld.features.start_page.start_page import StartPage
from helloworld.features.settings_page.settings_page import SettingsPage



dev_mode = True

class HelloWorld(App):
    def build(self):
        app_directory = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(app_directory, 'storage', 'user_data.json')
        screen_manager = ScreenManager()
        self.add_pages(screen_manager, app_directory)
        if dev_mode:
            screen_manager.current = 'dev_page'
            return screen_manager
        else:
            if os.path.isfile(file_path):
                screen_manager.current = 'start_page'
                return screen_manager
            else:
                screen_manager.current = 'data_page'
                return screen_manager

    def add_pages(self, screen_manager, app_directory):
        Builder.load_file(os.path.join(app_directory, 'features', 'dev_page', 'dev_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'diet_page', 'diet_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'start_page', 'start_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'training_plan_page', 'training_plan_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'data_page', 'user_data_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'gear_page', 'user_gear_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'goal_page', 'user_goal_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'place_page', 'user_place_page.kv'))
        Builder.load_file(os.path.join(app_directory, 'features', 'settings_page', 'settings_page.kv'))

        screen_manager.add_widget(DevPage(name='dev_page', path=app_directory))
        screen_manager.add_widget(StartPage(name='start_page', path=app_directory))
        screen_manager.add_widget(DietPage(name='diet_page', path=app_directory))
        screen_manager.add_widget(UserPlacePage(name='place_page', path=app_directory))
        screen_manager.add_widget(UserGearPage(name='gear_page', path=app_directory))
        screen_manager.add_widget(UserGoalPage(name='goal_page', path=app_directory))
        screen_manager.add_widget(UserDataPage(name='data_page', path=app_directory))
        screen_manager.add_widget(GeneratePlanPage(name='generate_plan', path=app_directory))
        screen_manager.add_widget(ExercisesPage(name='exercises', path=app_directory))
        screen_manager.add_widget(SettingsPage(name='settings_page', path=app_directory))


def main():
    HelloWorld().run()
