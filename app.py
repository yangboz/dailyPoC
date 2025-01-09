from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # 假设的 API 地址
DEEPSEEK_API_KEY = "sk-3fa454a083f848e898eaac95cb4f8932"  # 替换为你的 DeepSeek API 密钥

def call_deepseek_api(prompt):
    """调用 DeepSeek API 生成响应"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # 假设的模型名称
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "抱歉，我暂时无法处理你的请求。"

@app.route("/chat", methods=["POST"])


def generate_tip():
    """
    调用 DeepSeek API 生成 TIPS
    """
    try:
        # 记录开始时间
        start_time = time.time()

        # 请求体
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",  # 假设的模型名称
            "messages": [{"role": "user", "content": "生成一条 AI 学习 TIPS，简短一些。"}],
            "max_tokens": 50  # 限制生成内容的长度
        }

        # 调用 DeepSeek API
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功

        # 记录结束时间
        end_time = time.time()

        # 解析响应
        result = response.json()
        tip = result["choices"][0]["message"]["content"].strip()
        token_usage = result.get("usage", {}).get("total_tokens", 0)  # 获取 token 数量

        # 计算生成速度和费用
        generation_time = int((end_time - start_time) * 1000)  # 转换为毫秒
        cost = token_usage * TOKEN_PRICE  # 计算费用

        return {
            "tip": tip,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 生成时间点
            "generation_time": generation_time,  # 生成速度（毫秒）
            "token_usage": token_usage,  # token 数量
            "cost": round(cost, 4)  # 费用（保留 4 位小数）
        }
    except Exception as e:
        print(f"生成 TIPS 失败: {e}")
        return {
            "tip": "暂无 TIPS，请稍后再试。",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "generation_time": 0,
            "token_usage": 0,
            "cost": 0
        }

@app.route("/api/tips", methods=["GET"])
def get_tips():
    """
    提供 TIPS 数据的 API
    """
    tip_data = generate_tip()
    return jsonify(tip_data)

if __name__ == "__main__":
    app.run(debug=True)