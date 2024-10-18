import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

# API URL
url = 'https://api.youpin898.com/api/youpin/bff/trade/v1/trade/monitor/price/trend'

# 自定义请求头（根据需要）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyYTAyMTkzNjIxZDk0ZmNjOTNmMWM5NzdjOTUwNDIyMCIsIm5hbWVpZCI6Ijc2Njg1NDEiLCJJZCI6Ijc2Njg1NDEiLCJ1bmlxdWVfbmFtZSI6IkNpUGciLCJOYW1lIjoiQ2lQZyIsInZlcnNpb24iOiJiYTYiLCJuYmYiOjE3MjkwOTI2NTAsImV4cCI6MTcyOTk1NjY1MCwiaXNzIjoieW91cGluODk4LmNvbSIsImF1ZCI6InVzZXIifQ.baVdWU8aLDIwOUdyeqFeOKufkxJPfiv1iu0pNg58H6g'
}

# POST 请求体
data = {
    "templateId": "109794",
    "orderType": 1,
    "day": 30,
    #"day": 7,近七天记录
}

# 发送请求
response = requests.post(url, headers=headers, json=data)

# 检查请求是否成功
if response.status_code == 200:
    # 获取并解析JSON响应
    result = response.json()
    print(json.dumps(result, indent=4, ensure_ascii=False))
    
    # 提取 tradeDataList 中的 time, price, localDate
    trade_data = result.get("data", {}).get("tradeDataList", [])
    
    # 存储时间和价格
    times = []
    prices = []
    
    for trade in trade_data:
        time_stamp = trade["time"]
        price = float(trade["price"])
        local_date = trade["localDate"]
        
        # 将时间戳转换为可读的时间
        readable_time = datetime.fromtimestamp(time_stamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        
        # 存储转换后的时间和价格
        times.append(readable_time)
        prices.append(price)
    
    # 打印时间和价格
    for t, p in zip(times, prices):
        print(f"时间: {t}, 价格: {p}")
    
    # 找到极大值和极小值
    max_indices = [i for i in range(1, len(prices) - 1) if prices[i] > prices[i-1] and prices[i] > prices[i+1]]
    min_indices = [i for i in range(1, len(prices) - 1) if prices[i] < prices[i-1] and prices[i] < prices[i+1]]
    
    # 生成价格关于时间的折线图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号
    plt.figure(figsize=(10, 5))
    plt.plot(times, prices, marker='o', label="价格")

    # 在极大值和极小值处标注
    for i in max_indices:
        plt.axvline(x=times[i], color='red', linestyle='--', label='极大值' if i == max_indices[0] else "")
        plt.text(times[i], prices[i], f'{prices[i]:.2f}', color='red', verticalalignment='bottom')
    
    for i in min_indices:
        plt.axvline(x=times[i], color='blue', linestyle='--', label='极小值' if i == min_indices[0] else "")
        plt.text(times[i], prices[i], f'{prices[i]:.2f}', color='blue', verticalalignment='top')

    # 设置图表
    plt.xticks(rotation=45, ha='right')  # 时间标签旋转，避免重叠
    plt.xlabel("时间")
    plt.ylabel("价格")
    plt.title("半宝石")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # 显示图表
    plt.show()

else:
    print(f"请求失败，状态码: {response.status_code}")


