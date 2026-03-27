import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# --- 配置信息 ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_STATUS = "laundry/machine1/status"
TOPIC_EVENT = "laundry/machine1/event"
TOPIC_SNAPSHOT = "laundry/machine1/snapshot"

def get_now():
    return datetime.now().strftime("%H:%M:%S")

def publish_data(client, topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"[{get_now()}] [发送] Topic: {topic} | Data: {payload}")

# 使用 API VERSION2 消除警告
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

try:
    print(f"正在连接到公共服务器 {BROKER}...")
    client.connect(BROKER, PORT, 60)
    print("✅ 连接成功！开始循环模拟洗衣程序...\n")

    while True:  # 开启循环模拟
        # 1. 启动状态
        # 注意：Node-RED 中的 format_status 节点判断的是 'RUNNING'，
        # 我们可以把 STARTING/WASHING/SPINNING 都视为 RUNNING 状态
        publish_data(client, TOPIC_STATUS, {"state": "RUNNING", "detail": "STARTING"})
        publish_data(client, TOPIC_EVENT, {"event": "Door Locked", "time": get_now()})
        time.sleep(4)

        # 2. 洗涤过程
        publish_data(client, TOPIC_STATUS, {"state": "RUNNING", "detail": "WASHING"})
        publish_data(client, TOPIC_SNAPSHOT, {"state": "Agitating", "time": get_now()})
        time.sleep(6)

        # 3. 脱水过程
        publish_data(client, TOPIC_STATUS, {"state": "RUNNING", "detail": "SPINNING"})
        publish_data(client, TOPIC_EVENT, {"event": "High Speed Spin", "time": get_now()})
        time.sleep(6)

        # 4. 完成
        publish_data(client, TOPIC_STATUS, {"state": "IDLE", "detail": "FINISHED"})
        publish_data(client, TOPIC_EVENT, {"event": "Cycle Complete", "time": get_now()})
        publish_data(client, TOPIC_SNAPSHOT, {"state": "Idle", "time": get_now()})
        
        print("\n--- 一次洗涤循环结束，等待 10 秒开始下一次 ---\n")
        time.sleep(10)

except KeyboardInterrupt:
    print("\n用户停止模拟")
finally:
    client.disconnect()
    print("已断开连接")