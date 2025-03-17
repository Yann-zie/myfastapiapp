from openai import OpenAI  # Import OpenAI client
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class ChatGPTAPI:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("API key not found! Set the OPENAI_API_KEY environment variable.")
        
    def get_advice_from_chatgpt(self, category, user_input):
        client = OpenAI(api_key=self.openai_api_key)

        prompt = self.create_prompt(category, user_input)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
            ],
            model="gpt-3.5-turbo",
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    def create_prompt(self, category, user_input):
        return f"You are a helpful assistant offering advice in the category of {category}. " \
               f"The user asks: '{user_input}'. Please provide detailed advice."