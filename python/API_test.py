import os
import requests
from dotenv import load_dotenv

# 加载.env密钥文件
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def test_ai_request():
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "用JSON格式返回一句话，介绍requests库作用"}
        ],
        "response_format": {"type": "json_object"}
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        result = res.json()
        print("AI返回结果：")
        print(result["choices"][0]["message"]["content"])
    except Exception as err:
        print("调用失败：", err)

if __name__ == "__main__":
    test_ai_request()
