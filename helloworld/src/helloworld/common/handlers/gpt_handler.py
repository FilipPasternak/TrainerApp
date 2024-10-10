from openai import OpenAI
import os
import json
home_gym_equipment = {
    "Weights & Strength Training": [
        "Dumbbells",
        "Kettlebells",
        "Barbell",
        "Weight plates",
        "Medicine ball",
        "Sandbag",
        "Ankle weights"
    ],
    "Resistance & Bodyweight Training": [
        "Resistance bands",
        "TRX suspension trainer",
        "Resistance loop bands",
        "Push-up bars",
        "Parallette bars",
        "Core sliders"
    ],
    "Cardio Equipment": [
        "Treadmill",
        "Stationary bike",
        "Rowing machine",
        "Elliptical machine",
        "Jump rope",
        "Mini stepper",
        "Stepper"
    ],
    "Flexibility & Recovery": [
        "Yoga mat",
        "Foam roller",
        "Exercise ball",
        "Ab wheel",
        "Pull-up bar"
    ],
    "Power & Explosive Training": [
        "Plyo box",
        "Battle ropes"
    ],
    "Benches & Racks": [
        "Adjustable bench",
        "Power rack",
        "Squat rack"
    ]
}

class GptClient:
    def __init__(self, path):
        api_key=''
        self.client = OpenAI(api_key=api_key)
        self.path = path

    def chat(self, prompt, system):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            model="gpt-4o"
        )
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        return response.choices[0].message.content

    def generate_exercise_details(self, exercise, equipment, day, place):
        user_prompt = f"Provide a concise description for the exercise: {exercise} using: {equipment}."
        system_prompt = """
        You are a fitness expert who provides concise and clear exercise descriptions for a mobile app. 
        Your descriptions should be professional and easy to understand. 
        Each description should explain how to properly perform the exercise, including starting position, body movement, and focus on muscle groups.
        You should include correct way of doing this exercise to remove any misconceptions about doing it.
        The description should be no more than 2-3 sentences.
        After written description write number in scale 1-10 representing intensity of exercise and difficulty.
        After that write which muscles are most involved.
        example:
        Description|1|1|Muscles
        """
        details = {'Equipment': equipment}
        response = self.chat(prompt=user_prompt, system=system_prompt)
        response_splited = response.split(sep='|')
        details['Description'] = response_splited[0]
        details['Intensity'] = response_splited[1]
        details['Difficulty'] = response_splited[2]
        details['Muscles'] = response_splited[3]
        return {exercise: details}
