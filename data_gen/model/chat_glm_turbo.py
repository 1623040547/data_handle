import zhipuai

zhipuai.api_key = "48825887a45a0e06d4a374d77da2a330.R43SurxEuOMAJeYH"


def chat_glm_turbo(content, template=''):
    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": template},
            {"role": "assistant",
             "content": 'Please provide the sentences and keywords you need to rewrite and I will complete the rewrite for you.'},
            {"role": "user", "content": content},
        ],
    )
    return response['data']['choices'][0]['content']
