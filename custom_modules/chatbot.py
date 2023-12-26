import openai
import os

class ChatBot:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        openai.organization = "org-CoMvVF7wOctJ26QE1kfYBAqh"
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.message_history = []

    def ask(self, prompt):
        self.message_history.append({
            "role": "user",
            "content": prompt
        })
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.message_history
        )
        message = response["choices"][0]["message"]
        self.message_history.append(message)
        return message["content"]