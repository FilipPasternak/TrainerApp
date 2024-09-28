from TrainerApp.src.TrainerApp.features.pages.build_start_page import StartPage
from TrainerApp.src.TrainerApp.features.pages.build_diet_page import DietPage
from TrainerApp.src.TrainerApp.features.pages.build_training_plan_page import TrainingPlanPage

def go_to_start_page(widget):
    start_page = StartPage(widget.app.main_window)
    start_page.startup()

def go_to_diet_page(widget):
    diet_page = DietPage(widget.app.main_window)
    diet_page.startup()

def go_to_training_plan_page(widget):
    train_page = TrainingPlanPage(widget.app.main_window)
    train_page.startup()
