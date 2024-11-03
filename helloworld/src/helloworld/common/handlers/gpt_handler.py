import json
import os.path

from openai import OpenAI


class GptClient:
    def __init__(self, path):
        api_key=''
        self.client = OpenAI(api_key=api_key)
        self.path = path

    def chat(self, user, system):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": user
                }
            ],
            temperature=0.5,
            model="gpt-4o-mini"
        )
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        return response.choices[0].message.content

    def generate_exercise_details(self, exercise, equipment):
        user_prompt, system_prompt = self.get_exercise_details_prompt(exercise, equipment)
        details = {}
        response = self.chat(user=user_prompt, system=system_prompt)
        response_splited = response.split(sep='|')
        for i in range(len(response_splited)):
            if '\n\n' in response_splited[i]:
                response_splited[i] = response_splited[i].split('\n\n')[0]

        details['Equipment'] = response_splited[0]
        details['Description'] = response_splited[1]
        details['Intensity'] = response_splited[2]
        details['Difficulty'] = response_splited[3]
        details['Muscles'] = response_splited[4]
        return details

    def generate_plan(self, data):
        day_layout_system, day_layout_user = self.get_day_layout_prompts(data)
        day_layout_response = self.chat(system=day_layout_system, user=day_layout_user)

        exercise_plan_system, exercise_plan_user = self.get_exercise_plan_prompt(data, day_layout_response)
        exercise_plan_response = self.chat(system=exercise_plan_system, user=exercise_plan_user)

        workout_plan = self.parse_workout_plan(exercise_plan_response, day_layout_response)
        json_path = os.path.join(self.path, 'storage', 'workout_plan.json')
        with open(json_path, 'w') as file:
            json.dump(workout_plan, file, indent=4)

        return workout_plan

    def parse_workout_plan(self, response_plan, response_day_layout):
        '''
        Parses the workout plan and day layout strings, and returns a structured workout plan.

        :param response_plan: (str) Generated workout plan with exercises for corresponding days.
        :param response_day_layout: (str) Categories of workout for certain days.
        :return: (dict) Dictionary containing days as keys, and exercises mapped to workout categories as values.
        '''
        plan = {}

        # Clean up response strings
        response_plan = self.clean_response(response_plan)
        response_day_layout = self.clean_response(response_day_layout)

        # Process day layouts and exercises
        days_plan = response_plan.split("\n")
        days_layout = response_day_layout.split("\n")
        categories_exercises_layout = self.get_categories_exercises_layout(days_layout)

        for day in days_plan:
            if not day.strip():
                # Skip empty lines
                continue

            day_name, categories_exercises = self.process_day(day)
            day_plan = {}

            for idx, category_exercises in enumerate(categories_exercises):
                exercises = category_exercises.strip()
                day_plan[categories_exercises_layout[day_name][idx]] = exercises

            plan[day_name] = day_plan


        return plan

    @staticmethod
    def clean_response(response):
        '''Removes extra characters and trims newlines from the beginning and end of the response.'''
        return response.replace('```', '').strip()

    def get_categories_exercises_layout(self, days_layout):
        '''Generates a mapping of days to their corresponding workout categories.'''
        categories_exercises_layout = {}

        for day in days_layout:
            day_name, categories = day.split("-")
            day_name = self.map_days(day_name.strip())
            categories_list = [cat.rstrip() for cat in categories.split('|')]
            categories_exercises_layout[day_name] = categories_list

        return categories_exercises_layout

    def process_day(self, day):
        '''Splits a day's workout plan into the day name and the exercises for each category.'''
        day_parts = day.split(":")
        day_name = self.map_days(day_parts[0].strip()).rstrip()
        categories_exercises = day_parts[1].split("|")

        return day_name, categories_exercises

    @staticmethod
    def map_days(day_name):
        '''Maps full day names to short versions. Returns the original day_name if no match is found.'''
        day_map = {
            'Monday': 'Mon',
            'Tuesday': 'Tue',
            'Wednesday': 'Wed',
            'Thursday': 'Th',
            'Friday': 'Fri',
            'Saturday': 'Sat',
            'Sunday': 'Sun'
        }
        return day_map.get(day_name, day_name)

    def generate_exercise_description(self, exercise, equipment):
        user_prompt, system_prompt = self.get_exercise_details_prompt(exercise, equipment)
        return self.chat(user_prompt, system_prompt)

    @staticmethod
    def get_exercise_details_prompt(exercise, equipment):
        user_prompt = f"Provide a concise description for the exercise: {exercise} using: {equipment}."
        system_prompt = """
        You are a fitness expert who provides concise and clear exercise descriptions for a mobile app. 
        Your descriptions should be professional and easy to understand. 
        Each description should explain how to properly perform the exercise, including starting position, body movement, and focus on muscle groups.
        You should include correct way of doing this exercise to remove any misconceptions about doing it.
        The description should be no more than 2-3 sentences.
        Before the description, specify which piece of equipment is used for this exercise.
        ** Write only the name of equipment used! No additional words! **
        If none equipment is used, write Bodyweight.
        After written description write number in scale 1-10 representing intensity of exercise and difficulty.
        After that write which muscles are most involved.
        ** IT IS VERY IMPORTANT TO NOT ADD ANY ADDITIONAL WORDS IN YOUR ANSWER. FOLLOW THIS FORMAT IN EXAMPLE **
        example:
        Used equipment|Description|1|1|Muscles
        """
        return user_prompt, system_prompt

    @staticmethod
    def get_day_layout_prompts(data):
        day_layout_user = f"""
        Build a weekly workout plan for these days: {data['Frequency']}. It is for {data['Sex']}.
        Use [Push day, Pull day, Leg day, Core and cardio].
        If two categories are assigned for one day, separate them with `|`.
        **Do not add any extra text or explanations.**
        Follow this format exactly:
        Fri-Push day
        Sat-Pull day|Core and cardio
        Sun-Leg day
        """

        day_layout_system = """
        You are a professional personal trainer.
        Create a balanced weekly workout using these categories:
        - Push day
        - Pull day
        - Leg day
        - Core and cardio
        If two categories are needed for one day, separate them with `|`.
        **Provide only the workout plan and avoid any additional explanations or comments.**
        **Do not add any additional characters like ` or '. Type only what is in given format, line by line.
        Follow this exact format: Day-Category.
        """
        return day_layout_system, day_layout_user

    @staticmethod
    def get_exercise_plan_prompt(data, day_layout_response):
        exercise_plan_user = f"""
        Create a weekly workout plan based on this schedule: {day_layout_response}.
        If there are two categories of workout in the same day, they will be separated by '|', and you shall generate exercises for both categories.
        User details:
        - Gender: {data['Sex']}
        - Age: {data['Age']}
        - Workout location: {data['Place']}
        - Available equipment: {data['User_gear']}
        - Experience level: {data['Experience']}
        - Preferred intensity: {data['Intensity']}

        For each day, select an appropriate number of exercises based on the workout category:
        - Push day: 9-12 exercises (focus on chest, shoulders, and triceps)
        - Pull day: 9-12 exercises (focus on back, biceps, and rear delts)
        - Leg day: 9-13 exercises (focus on quads, hamstrings, glutes, and calves)
        - Core and cardio: 7-9 exercises (focus on abs, endurance, and stability)

        Ensure the exercises create a balanced workout that targets the key muscles for each category.
        **DO NOT** add any extra explanation or text other than the exercise names in the required format.

        For days with two categories, separate exercises for each category using '|' between them.
        Use short versions of days (Fri, Sat, Sun) NOT FULL DAY NAMES.
        Provide the exercises in **this exact format (USE SPACES IN EXERCISES NAMES)**:
        Day:exercise one,exercise two,exercise three|exercise four,exercise five,exercise six (no spaces between commas, and no extra text).
        """

        exercise_plan_system = """
        You are a professional personal trainer.
        Based on the provided schedule and user details (gender, age, workout location, available equipment, experience level, and preferred intensity),
        create a well-structured weekly workout plan.
        For each day, assign an appropriate number of exercises according to the workout category for that day:
        - Push day: 9-12 exercises (chest, shoulders, triceps)
        - Pull day: 9-12 exercises (back, biceps, rear delts)
        - Leg day: 9-13 exercises (quads, hamstrings, glutes, calves)
        - Core and cardio: 7-9 exercises (abs, endurance)

        **Only provide exercises. Do not include explanations or comments.**

        For days with two categories, use '|' to separate exercises for each category.
        Use this exact format for the output:  
        Day:exercise1,exercise2,exercise3|exercise4,exercise5,exercise6 (no spaces between commas, and no additional text).
        """

        return exercise_plan_system, exercise_plan_user

# with open(r'C:\Users\revte\Desktop\Inzynierka\helloworld\src\helloworld\storage\user_data.json', 'r') as file:
#     data = json.load(file)
#
# client = GptClient(r'C:\Users\revte\Desktop\Inzynierka\helloworld\src\helloworld')
# plan = client.generate_plan(data)
#
# dupa = 1