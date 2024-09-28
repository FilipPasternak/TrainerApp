from helloworld.features.pages.build_start_page import StartPage
from helloworld.features.pages.build_diet_page import DietPage
from helloworld.features.pages.build_training_plan_page import TrainingPlanPage
from helloworld.features.pages.build_first_run_user_gear_page import FirstRunUserGearPage
import csv
import os

pages_dict = {'start': StartPage,
              'diet': DietPage,
              'training_plan': TrainingPlanPage,
              'first_run_user_gear': FirstRunUserGearPage}

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

def go_to_first_run_user_gear_page(widget):
    build_first_run_user_gear_page = FirstRunUserGearPage(widget.app.main_window)
    build_first_run_user_gear_page.startup()
