#Video Reference: Create a Python GPT Chatbot - In Under 4 Minutes.
#https://www.youtube.com/watch?v=q5HiD5PNuck.
#CopyPasted Code.

import openai

openai.api_key = ""

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You:")
        if user_input.lower() in ["quit","exit","bye"]:
            break

        response = chat_with_gpt(user_input)
        print("ChatBot: ", response)
