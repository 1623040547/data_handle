import requests
import json

API_KEY = "G4NSXoVliH9YiMRPblRCCSfL"
SECRET_KEY = "X2sxRIfDqkyld1oftrmOjZovraiHsnQZ"


class Llama:
    def __init__(self):
        self.token = ""

    def llama_70_chat(self, content, template: str):
        if self.token == "":
            self.token = get_access_token()
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_2_70b?access_token=" + self.token

        payload = json.dumps({
            "messages": [
                {"role": "user", "content": template},
                {"role": "assistant", "content": "Please provide your original sentences and the corresponding keywords, and I will generate the rewritten sentences accordingly."},
                {"role": "user", "content": content},
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json().get('result')


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    key = requests.post(url, params=params, headers=headers, data=payload)
    print(key.json().get("access_token"))
    return str(key.json().get("access_token"))
