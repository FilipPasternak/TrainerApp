import pytest
from helloworld.common.handlers.gpt_handler import GptClient

test_data = {
    "Name": "Filip",
    "Sex": "Man",
    "Age": "21",
    "Weight": "74",
    "Height": "184",
    "Place": "At home with equipment",
    "User_gear": [
        "Dumbbells",
        "Kettlebells",
        "Barbell",
        "Weight plates",
        "Yoga mat",
        "Foam roller",
        "Exercise ball",
        "Plyo box",
        "Battle ropes"
    ],
    "Experience": "Working out regularly",
    "Goal": "Gain muscle",
    "Intensity": "Medium",
    "Frequency": [
        "Tue",
        "Wed",
        "Fri"
    ]
}

client = GptClient('test')

def test_generate_plan_multiple_runs():
    error_count = 0
    for i in range(1000):
        try:
            day_layout_system, day_layout_user = client.get_day_layout_prompts(test_data)
            day_layout_response = client.chat(system=day_layout_system, user=day_layout_user)
            exercise_plan_system, exercise_plan_user = client.get_exercise_plan_prompt(test_data, day_layout_response)
            exercise_plan_response = client.chat(system=exercise_plan_system, user=exercise_plan_user)
            plan = parse_workout_plan(exercise_plan_response, day_layout_response)
        except Exception as e:
            print('Error')
            try:
                parse_workout_plan(exercise_plan_response, day_layout_response)
            except:
                pass
            error_count += 1
            with open(f"error_log_{i}.txt", "w") as f:
                f.write(f"Error in iteration {i}:\n")
                f.write(f"Day layout response:\n{day_layout_response}\n")
                f.write(f"Exercise plan response:\n{exercise_plan_response}\n")
                f.write(f"Error message: {str(e)}\n")

    assert error_count == 0, f"{error_count} errors occurred during the 10 test iterations."


def parse_workout_plan(response_plan, response_day_layout):
    '''
    Parses the workout plan and day layout strings, and returns a structured workout plan.

    :param response_plan: (str) Generated workout plan with exercises for corresponding days.
    :param response_day_layout: (str) Categories of workout for certain days.
    :return: (dict) Dictionary containing days as keys, and exercises mapped to workout categories as values.
    '''
    plan = {}

    # Clean up response strings
    response_plan = clean_response(response_plan)
    response_day_layout = clean_response(response_day_layout)

    # Process day layouts and exercises
    days_plan = response_plan.split("\n")
    days_layout = response_day_layout.split("\n")
    categories_exercises_layout = get_categories_exercises_layout(days_layout)

    for day in days_plan:
        if not day.strip():
            # Skip empty lines
            continue

        day_name, categories_exercises = process_day(day)
        day_plan = {}

        for idx, category_exercises in enumerate(categories_exercises):
            exercises = category_exercises.strip()
            day_plan[categories_exercises_layout[day_name][idx]] = exercises

        plan[day_name] = day_plan

    return plan


def clean_response(response):
    '''Removes extra characters and trims newlines from the beginning and end of the response.'''
    return response.replace('```', '').strip()


def get_categories_exercises_layout(days_layout):
    '''Generates a mapping of days to their corresponding workout categories.'''
    categories_exercises_layout = {}

    for day in days_layout:
        day_name, categories = day.split("-")
        day_name = map_days(day_name.strip())
        categories_exercises_layout[day_name] = categories.split('|')

    return categories_exercises_layout


def process_day(day):
    '''Splits a day's workout plan into the day name and the exercises for each category.'''
    day_parts = day.split(":")
    day_name = map_days(day_parts[0].strip())
    categories_exercises = day_parts[1].split("|")

    return day_name, categories_exercises


def map_days(day_name):
    '''Maps full day names to short versions. Returns the original day_name if no match is found.'''
    day_map = {
        'Monday': 'Mon',
        'Tuesday': 'Tue',
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
    }
    return day_map.get(day_name, day_name)


test_generate_plan_multiple_runs()