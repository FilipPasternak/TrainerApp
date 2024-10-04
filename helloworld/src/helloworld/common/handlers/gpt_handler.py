from openai import OpenAI
import os

class GptClient:
    def __init__(self, path):
        api_key=''
        self.client = OpenAI(api_key=api_key)
        self.path = path

    def chat_test(self):
        answer = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.read_prompt_from_txt('test_template')
                }
            ],
            model="gpt-3.5-turbo"
        )
        return answer.choices[0].message.content

    def read_prompt_from_txt(self, template):
        file_path = os.path.join(self.path, 'common', 'handlers', 'gpt_prompts_templates', 'prompts.txt')
        choose_template = {
            'test_template': 1
        }
        template_idx = choose_template[template]

        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines[template_idx - 1].strip()


client = GptClient(r'C:\Users\revte\Desktop\Inzynierka\helloworld\src\helloworld')
print(client.chat_test())