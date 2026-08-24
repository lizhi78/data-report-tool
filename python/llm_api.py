import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"

# 启动校验密钥
if not API_KEY:
    raise ValueError("缺少 DEEPSEEK_API_KEY，请检查 .env 文件配置！")

def chat_with_ai(user_content, system_prompt="你是数据分析专家，严格输出标准JSON，不要额外说明文字"):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "deepseek-chat",
        "temperature": 0.2,
        # API官方参数 response_format：强制模型输出合法JSON字符串
        # 相比单纯prompt约束更加稳定，禁止模型输出多余描述、markdown标记
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    }

    try:
        resp = requests.post(URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()

        if "error" in result:
            return {"status": False, "msg": f"【API业务报错】{result['error'].get('message', '未知接口错误')}", "data": None}

        raw_answer = result["choices"][0]["message"]["content"]
        # response_format保证raw_answer是标准JSON，直接解析
        json_data = json.loads(raw_answer)
        return {"status": True, "msg": "success", "data": json_data}

    except json.JSONDecodeError:
        return {"status": False, "msg": "【失败】模型返回内容不是合法JSON", "data": None}
    except requests.exceptions.Timeout:
        return {"status": False, "msg": "【失败】请求超时：服务器响应缓慢，请重试", "data": None}
    except requests.exceptions.ConnectionError:
        return {"status": False, "msg": "【失败】网络异常：无法连接DeepSeek服务器，请检查网络", "data": None}
    except requests.exceptions.HTTPError as e:
        return {"status": False, "msg": f"【失败】HTTP请求错误：{str(e)}", "data": None}
    except (KeyError, IndexError):
        return {"status": False, "msg": "【失败】接口返回数据格式异常，解析失败", "data": None}
    except Exception as e:
        return {"status": False, "msg": f"【失败】未知异常：{str(e)}", "data": None}
