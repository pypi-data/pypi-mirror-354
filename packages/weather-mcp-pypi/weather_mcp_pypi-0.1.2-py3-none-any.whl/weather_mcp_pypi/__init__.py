import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather",host="10.11.28.180",port=8878)

API_KEY = "7fee5af3022b2eada36c04f33c41d69e"  # 聚合AK
BASE_URL = "http://apis.juhe.cn/simpleWeather/query"


@mcp.tool()
def get_weather(location: str) -> str:
    """获取指定地点的天气预报。
    参数：
        location (str): 城市名。
    返回：
        str: 天气信息。
    """
    try:

        params = {
            "city": location,
            "key": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()


        # 解析聚合返回数据
        weather_data = response.json()['result']
        city = weather_data["city"]
        real_data = weather_data['realtime']
        real = {}
        real['temperature'] = real_data['temperature']
        real['humidity'] = real_data['humidity']
        real['direct'] = real_data['direct']
        real['power'] = real_data['power']
        future = {}
        future_data = weather_data['future']
        str = (
            f"{city}的天气：{real['direct']}，风力{real['power']}，温度 {real['temperature']}°C，湿度是{real['humidity']}\n\n"
            f"未来{len(future_data)}天,天气是：\n")
        for info in future_data:
            str += f"{info['date']}：{info['weather']}，温度：{info['temperature']}\n"

        return str


    except requests.RequestException as e:
        return f"获取天气信息失败：{str(e)}"



def main() -> None:
    mcp.run(transport="stdio")
