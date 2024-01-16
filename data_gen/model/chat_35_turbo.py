import openai

openai.api_key = "sk-7Tb8H2iJCUZKA0NXkXYkJB14UnMKXCZiGfAZ5srTnOWko9gs"
openai.api_base = "https://api.chatanywhere.com.cn/v1"


def chat_35_turbo(content, template: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                {"role": "user", "content": template},
                {"role": "assistant",
                 "content": 'yes'},
                {"role": "user", "content": content},
            }
        ],
    )
    return completion.choices[0].message.content
