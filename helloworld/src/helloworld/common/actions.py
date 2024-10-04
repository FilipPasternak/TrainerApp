from helloworld.features.pages.build_start_page import StartPage
from helloworld.features.pages.build_diet_page import DietPage
from helloworld.features.pages.build_training_plan_page import TrainingPlanPage
from helloworld.features.pages.build_first_run_user_place_page import FirstRunUserPlacePage
from helloworld.features.pages.build_user_gear_page import UserGearPage
from helloworld.features.pages.build_user_goal_page import UserGoalPage
from helloworld.features.pages.build_first_run_user_data_page import FirstRunUserDataPage
from helloworld.features.pages.dev_page import DevPage


def go_to_start_page(widget):
    page = StartPage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_diet_page(widget):
    page = DietPage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_training_plan_page(widget):
    page = TrainingPlanPage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_first_run_user_place_page(widget):
    page = FirstRunUserPlacePage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_user_gear_page(widget):
    page = UserGearPage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_user_goal_page(widget):
    page = UserGoalPage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_user_data_page(widget):
    page = FirstRunUserDataPage(widget.app.main_window, widget.app.paths.app)
    page.startup()

def go_to_dev_page(widget):
    page = DevPage(widget.app.main_window, widget.app.paths.app)
    page.startup()
