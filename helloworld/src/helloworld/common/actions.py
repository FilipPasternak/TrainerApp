from helloworld.features.pages.build_start_page import StartPage
from helloworld.features.pages.build_diet_page import DietPage
from helloworld.features.pages.build_training_plan_page import TrainingPlanPage
from helloworld.features.pages.build_first_run_user_place_page import FirstRunUserPlacePage
from helloworld.features.pages.build_user_gear_page import UserGearPage
from helloworld.features.pages.build_user_goal_page import UserGoalPage


def go_to_start_page(widget):
    print(widget.app.paths.app)
    start_page = StartPage(widget.app.main_window, widget.app.paths.app)
    start_page.startup()

def go_to_diet_page(widget):
    diet_page = DietPage(widget.app.main_window, widget.app.paths.app)
    diet_page.startup()

def go_to_training_plan_page(widget):
    train_page = TrainingPlanPage(widget.app.main_window, widget.app.paths.app)
    train_page.startup()

def go_to_first_run_user_place_page(widget):
    build_first_run_user_place_page = FirstRunUserPlacePage(widget.app.main_window, widget.app.paths.app)
    build_first_run_user_place_page.startup()

def go_to_user_gear_page(widget):
    build_user_gear_page = UserGearPage(widget.app.main_window, widget.app.paths.app)
    build_user_gear_page.startup()

def go_to_user_goal_page(widget):
    build_user_goal_page = UserGoalPage(widget.app.main_window, widget.app.paths.app)
    build_user_goal_page.startup()
