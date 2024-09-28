"""
My first application
"""

import toga
from TrainerApp.src.TrainerApp.features.pages.build_start_page import StartPage
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class Filip(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        self.main_window = toga.MainWindow(title=self.formal_name)
        start_page = StartPage(self.main_window)
        start_page.startup()


def main():
    return Filip()
