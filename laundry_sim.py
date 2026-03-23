import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# 配置信息 (与你的 Node-RED 配置一致)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_STATUS = "laundry/machine1/status"
TOPIC_EVENT = "laundry/machine1/event"
TOPIC_SNAPSHOT = "laundry/machine1/snapshot"

def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def publish_data(client, topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"[发送] Topic: {topic} | Data: {payload}")

# 实例化 MQTT 客户端
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

try:
    print("--- 开始模拟洗衣程序 ---")

    # 1. 启动状态
    publish_data(client, TOPIC_STATUS, {"state": "STARTING", "time": get_now()})
    publish_data(client, TOPIC_EVENT, {"event": "Door Locked", "time": get_now()})
    time.sleep(3)

    # 2. 洗涤过程
    publish_data(client, TOPIC_STATUS, {"state": "WASHING", "time": get_now()})
    publish_data(client, TOPIC_SNAPSHOT, {"state": "Agitating", "time": get_now()})
    time.sleep(5)

    # 3. 脱水过程
    publish_data(client, TOPIC_STATUS, {"state": "SPINNING", "time": get_now()})
    publish_data(client, TOPIC_EVENT, {"event": "High Speed Spin", "time": get_now()})
    time.sleep(5)

    # 4. 完成
    publish_data(client, TOPIC_STATUS, {"state": "FINISHED", "time": get_now()})
    publish_data(client, TOPIC_EVENT, {"event": "Cycle Complete", "time": get_now()})
    publish_data(client, TOPIC_SNAPSHOT, {"state": "Idle", "time": get_now()})

    print("--- 模拟结束 ---")

except KeyboardInterrupt:
    print("用户停止模拟")
finally:
    client.disconnect()