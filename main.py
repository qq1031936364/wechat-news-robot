import requests
import json
from datetime import datetime

# -------- 配置信息 无需修改 --------
# 方糖推送密钥
SENDKEY = "SCT345196TaOHNDhaah7GgGb7x3PaGiDMn"
# 火山方舟豆包密钥
DOUBAO_API_KEY = "api-key-20260504114628"
DOUBAO_ENDPOINT_ID = "ark-e7e6f3a5-e869-44ca-82b1-24d7f1d956a0-5ea88"
API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

# 监控关键词
QUERY_LIST = [
    "当月下月 影响生产生活 重大政策 民生热点事件",
    "A股行业缺货涨价 产业链紧缺环节 最新动态",
    "光模块 800G 1.6T 浪潮信息 工业富联 永鼎股份 行业订单产能",
    "AI服务器 液冷 储能 电力 迎峰度夏 政策与供需",
    "半导体 光刻胶 锂电材料 供需缺口 利好个股"
]

# 组装提示词
def make_prompt():
    queries = "\n".join(QUERY_LIST)
    prompt = f"""
请基于以下方向做完整版专业分析：
{queries}

严格按固定格式输出，不冗余、不闲聊：
【播报时间】年月日 时分
【重大政策/热点事件】当月+下月关键事件、落地时间、对生产生活影响
【受影响行业】分利好、利空分别列出
【缺货紧缺产业链】写明品种、紧缺原因、紧张程度
【利好核心个股】分行业标注标的+一句核心炒作逻辑

要求：贴合A股投资实战，精简干货。
"""
    return prompt

# 调用火山豆包大模型
def get_doubao_news():
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DOUBAO_ENDPOINT_ID,
        "messages": [
            {"role": "user", "content": make_prompt()}
        ],
        "temperature": 0.3
    }
    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        res_json = res.json()
        content = res_json["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        return f"⚠️ 资讯获取失败：{str(e)}"

# 推送到微信（方糖）
def push_to_wechat(content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = f"🕒 整点行业资讯 | {now}"
    url = f"https://sct.ftqq.com/{SENDKEY}.send"
    data = {
        "title": title,
        "desp": content
    }
    requests.post(url, data=data)

# 主函数
def main():
    news_content = get_doubao_news()
    push_to_wechat(news_content)

if __name__ == "__main__":
    main()
