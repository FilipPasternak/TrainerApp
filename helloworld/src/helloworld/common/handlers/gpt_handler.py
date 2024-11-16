import json
import os.path
from datetime import datetime
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

        if len(response_splited) != 5:
            return self.generate_exercise_details(exercise, equipment)

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
        workout_plan['Date'] = datetime.today().strftime('%Y-%m-%d')
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

    def generate_diet(self, data):
        user, system = self.get_diet_plan_prompt(data)
        response = self.chat(user, system)
        response_dict = self.parse_dict_response(response)

        recipes_path = os.path.join(self.path, 'storage', 'recipes.json')
        diet_path = os.path.join(self.path, 'storage', 'diet.json')
        with open(recipes_path, 'r') as file:
            existing_recipes = json.load(file)

        for day in response_dict:
            for dish in response_dict[day]:
                if dish not in existing_recipes['Recipes'].keys():
                    user_details, system_details = self.get_dish_details_prompt(data, dish)
                    details_dict = None
                    while details_dict is None:
                        details_response = self.chat(user_details, system_details)
                        details_dict = self.parse_dict_response(details_response)
                    existing_recipes['Recipes'][dish] = details_dict

        with open(recipes_path, 'w') as file:
            json.dump(existing_recipes, file, indent=4)

        with open(diet_path, 'w') as file:
            json.dump(response_dict, file, indent=4)


    def parse_dict_response(self, response):
        response = response.strip("```python\n").rstrip("\n```").strip('\n')
        response = response.replace("(", "[").replace(")", "]").replace("'", "\"")

        try:
            diet_plan = json.loads(response)
            return diet_plan
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None


    def generate_training(self, plan, day, descriptions):
        training_details = {}
        for workout_name, exercises_str in plan[day].items():
            exercises_list = [exercise.strip() for exercise in exercises_str.split(',')]
            for exercise in exercises_list:
                training_details[exercise] = {}
                system, user = self.get_training_mode_prompt(exercise, descriptions[exercise]["Equipment"])
                response = self.chat(user, system)
                response_listed = response.split('|')
                training_details[exercise]['Series'] = response_listed[0].split('x')[0]
                training_details[exercise]['Reps'] = response_listed[0].split('x')[1]
                training_details[exercise]['Rest'] = response_listed[1]
                training_details[exercise]['Weight'] = response_listed[2]
                training_details[exercise]['Series time'] = response_listed[3]

        return training_details



    @staticmethod
    def get_exercise_details_prompt(exercise, equipment):
        user_prompt = f"Provide a concise description for the exercise: {exercise} using: {equipment}." \
                      f"**Choose only one piece of equipment from list**"
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

    def get_diet_plan_prompt(self, data):
        diet_plan_user = f'''
        User details:
        - Gender: {data['Sex']}
        - Age: {data['Age']}
        - Weight: {data['Weight']}kg
        - Height: {data['Height']}cm
        - User goal: {data['Goal']}
        Generate full 5 meals a day diet for provided user. Write it in form of python dictionary using this format:
        {'{ day_name: [dish name for breafast, dish name for 2nd breakfast ...]}'}.
        For each day prepare one easy to do at home dish for each of 5 meals, that is: Breakfast, 2dn Breakfast, DInner, Snack, Supper.
        Do not include names of the meals just the dishes. 
        Generate diet for all days in week.
        * DO NOT INCLUDE ANY OTHER ADDITIONAL COMMENTS, REPLIES OR ANYTHING THAT IS NOT THIS DICTIONARY *
                * IMPORTANT Use double quotes *

        '''

        diet_plan_system = f'''
        You are professional sport diet expert. You are to provide fully nutritious meals to meet user needs.
        You stick to more traditional diets, not over-using the almond milk and other modern things
        '''
        return diet_plan_user, diet_plan_system

    def get_dish_details_prompt(self, data, dish):
        response_format = {
            'Instruction': 'Instructions provided by you',
            'Ingredients': 'List of tuples, eg. (flour, 400g), (chicken 400g)',
            'Nutrients': 'List of tuples, eg. (protein, 20g), (calories, 440kcal)'
        }
        dish_details_user = f'''
       User details:
        - Gender: {data['Sex']}
        - Age: {data['Age']}
        - Weight: {data['Weight']}kg
        - Height: {data['Height']}cm
        - User goal: {data['Goal']}
        For provided user, prepare step by step instruction for preparing this dish.
        Prepare how much of those ingredients is needed, and how many nutrients it would be.
        For instructions be very concise and include only most important informations.
        All those details must be provided in form of python dictionary.
        Follow this format:
        {response_format}
        Include more of the most important nutrients that I provided you with this example.
        * IMPORTANT Use double quotes *
        '''

        dish_details_system = f"""
        You are an expert culinary assistant specializing in nutrition and meal preparation. 
        Your task is to generate a concise and detailed breakdown for the preparation of the dish '{dish}' based on user information provided.

        Details to include:
        - Step-by-step **Instructions**: Write these concisely, highlighting only the essential steps for preparing the dish.
        - **Ingredients**: Provide a list of ingredients in tuples, each containing the ingredient name and quantity. 
        - **Nutrients**: Include a list of nutrient tuples, focusing on important dietary values such as protein, calories, fats, carbohydrates, and vitamins.
        """

        return dish_details_user, dish_details_system


    @staticmethod
    def get_training_mode_prompt(exercise, equipment):
        system_prompt = '''
                    You are a professional personal trainer.
                    
                    Based on the provided exercise name and available equipment, provide specific information on how the exercise should be executed.
                    
                    **Instructions:**
                    
                    - **Response Format:** Your response must adhere **exactly** to the following format:
                    (series)x(reps or time)|(rest between series)|(suggested weight or 'None')|(average time per series)
                    - **Series and Repetitions:**
                    - For repetition-based exercises: Use the format `(number of series)x(number of reps)`.
                      - Example: `3x12`
                    - For time-based exercises: Use the format `(number of series)x(time in seconds)`.
                      - Example: `3x60s`
                    
                    - **Rest Between Series:**
                    - Specify the rest time between series in seconds, followed by `s`.
                      - Example: `30s`
                    
                    - **Suggested Weight:**
                    - If the exercise involves machines or free weights, include the suggested weight followed by the unit (e.g., `kg`).
                      - Example: `20kg`
                    - If no weight is involved, write `None`.
                    
                    - **Average Time per Series:**
                    - Provide the average time for one series in seconds, followed by `s`.
                      - Example: `60s`
                    
                    - **Example Response:**
                    3x8|30s|25kg|60s
                    
                    **Important:**
                    
                    - **Do not include** any additional text, explanations, or salutations.
                    - **Only output** the required information in the specified format.

                '''

        user_prompt = f'''
        Exercise: {exercise}
        Equipment available: {equipment}
        '''

        return user_prompt, system_prompt


# with open(r'C:\Users\revte\Desktop\Inzynierka\helloworld\src\helloworld\storage\user_data.json', 'r') as file:
#     data = json.load(file)
#
# client = GptClient(r'C:\Users\revte\Desktop\Inzynierka\helloworld\src\helloworld')
# client.generate_diet(data)
# dupa = 1