"""
My first application
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from helloworld.features.pages.build_start_page import StartPage
from helloworld.features.pages.build_first_run_user_data_page import FirstRunUserDataPage

import os


class HelloWorld(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        file_path = os.path.join(self.paths.app, 'storage', 'user_data.csv')
        self.main_window = toga.MainWindow(title=self.formal_name)

        if os.path.isfile(file_path):
            start_page = StartPage(self.main_window, self.paths.app)
            start_page.startup()
        else:
            first_run_page = FirstRunUserDataPage(self.main_window, self.paths.app)
            first_run_page.startup()


def main():
    return HelloWorld()
