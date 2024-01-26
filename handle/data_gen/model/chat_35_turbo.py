from openai import OpenAI

client = OpenAI(
    api_key="sk-MtfR4Vof32KoaYSE4a9a65F1F8Db478d857588126fD6Ef4e",
    base_url="https://cd.aiskt.com/v1"
)


# openai.api_key = "sk-7Tb8H2iJCUZKA0NXkXYkJB14UnMKXCZiGfAZ5srTnOWko9gs"
# openai.api_base = "https://api.chatanywhere.com.cn/v1"


def chat_35_turbo(content, template: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": template},
            {"role": "assistant",
             "content": 'yes'},
            {"role": "user", "content": content},
        ],
    )
    return completion.choices[0].message.content
