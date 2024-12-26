import asyncio
import threading
import time
from Adafruit_IO import MQTTClient
from ai import image_detector
from server import websocket_server, start_http_server, open_browser

AIO_FEED_IDs = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = ""
AIO_KEY = ""

def connected(client):
    print("Kết nối thành công...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thành công...")

def disconnected(client):
    print("Ngắt kết nối...")
    sys.exit(1)

def message(client, feed_id, payload):
    print("Nhận dữ liệu: " + payload + " từ feed_id: " + feed_id)

# MQTT Client
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

# Nhận diện hình ảnh trong vòng lặp chính
async def face_detection_loop():
    counter_ai = 3
    while True:
        counter_ai -= 1
        if counter_ai <= 0:
            counter_ai = 3
            ai_result = image_detector()
            print("AI Output:", ai_result)
            if ai_result != 0:
                client.publish("ai", ai_result)
        await asyncio.sleep(1)

# Chương trình chính
async def main():
    # Chạy HTTP server trong luồng riêng
    threading.Thread(target=start_http_server, daemon=True).start()

    # Mở trình duyệt
    open_browser()

    # Chạy song song WebSocket server và vòng lặp nhận diện
    await asyncio.gather(
        websocket_server(),   # WebSocket server
        face_detection_loop() # Nhận diện khuôn mặt
    )

if __name__ == "__main__":
    asyncio.run(main())