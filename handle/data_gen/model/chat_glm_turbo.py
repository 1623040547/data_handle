import zhipuai

zhipuai.api_key = "48825887a45a0e06d4a374d77da2a330.R43SurxEuOMAJeYH"


def chat_glm_turbo(content, template=''):
    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": template},
            {"role": "assistant",
             "content": 'yes'},
            {"role": "user", "content": content},
        ],
    )
    return response['data']['choices'][0]['content']
