import requests
from datetime import datetime

# 你的方糖SendKey
SENDKEY = "SCT345196TaOHNDhaah7GgGb7x3PaGiDMn"

# 监控搜索关键词列表
QUERY_LIST = [
    "当月下月 影响生产生活 重大政策 民生事件",
    "A股近期缺货涨价行业 产业链紧缺环节",
    "光模块 800G 1.6T 浪潮信息 工业富联 永鼎股份 最新行业动态",
    "AI服务器 液冷 储能 电力 迎峰度夏 政策供需",
    "半导体 光刻胶 锂电材料 缺货 利好个股"
]

# 组装提问话术
def make_prompt():
    queries = "\n".join(QUERY_LIST)
    prompt = f"""
请基于以下方向做完整复盘分析：
{queries}

严格按固定格式输出，不要多余废话：
【播报时间】年月日时分
【重大政策/热点事件】当月+下月关键事件、落地影响
【受影响行业】利好/利空分开列
【缺货紧缺产业链】写明品种、原因、紧张程度
【利好核心个股】分行业标注标的+一句核心逻辑

要求：贴合A股实战，内容精炼、专业、有参考价值。
"""
    return prompt

# 调用豆包获取资讯
def get_news():
    url = "https://api.doubao.com/v1/chat/completions"
    payload = {
        "model":"doubao-lite",
        "messages":[{"role":"user","content":make_prompt()}],
        "temperature":0.3
    }
    try:
        res = requests.post(url, json=payload, timeout=80)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"资讯获取失败：{str(e)}"

# 推送到微信方糖
def push_wechat(content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = f"整点行业资讯｜{now}"
    api = f"https://sct.ftqq.com/{SENDKEY}.send"
    data = {"title":title, "desp":content}
    requests.post(api, data=data)

# 主运行
def main():
    news = get_news()
    push_wechat(news)

if __name__ == "__main__":
    main()
