import sys
import asyncio
import websockets
import threading
import webbrowser
import json  # Import thư viện json để xử lý dữ liệu JSON
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from Adafruit_IO import MQTTClient

AIO_FEED_IDs = []
AIO_USERNAME = ""
AIO_KEY = ""


def connected(client):
    print("Ket noi thanh cong...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

# def message(client, feed_id, payload):
#     print("Nhan du lieu: " + payload + "feed_id:" + feed_id)


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
# client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

audio_flag = 0
max_flag = 0
audio_key = ""

# Hàm xử lý dữ liệu từ WebSocket client
async def receive_audio_data(websocket):
    global audio_flag
    global audio_key
    print("WebSocket connection established")
    try:
        async for message in websocket:
            data = json.loads(message)  # Chuyển dữ liệu JSON thành dictionary
            max_key = max(data, key=data.get)  # Tìm key có giá trị lớn nhất
            max_value = data[max_key]  # Giá trị tương ứng
            print(f"{float(max_value) * 100:.0f}% {max_key}")  # In ra tỉ lệ % và key
            if max_key == "OK MY HOME":
                audio_flag = 1
                audio_key = max_key
            elif audio_flag == 1 and max_key != "Background Noise" and max_key != "Others":
                audio_flag = 0
                audio_key = max_key
            if audio_key != "":
                client.publish("audio", audio_key)
                audio_key = ""
    except Exception as e:
        print("Error:", e)

# Chạy WebSocket server
async def websocket_server():
    async with websockets.serve(receive_audio_data, "localhost", 8000):
        print("WebSocket server is running on ws://localhost:8000")
        await asyncio.Future()  # Chạy vô thời hạn

# HTTP server để phục vụ HTML
def start_http_server():
    PORT = 8080
    Handler = SimpleHTTPRequestHandler
    with TCPServer(("localhost", PORT), Handler) as httpd:
        print(f"HTTP server serving at http://localhost:{PORT}")
        httpd.serve_forever()

# Tự động mở trình duyệt với file HTML
def open_browser():
    url = "http://localhost:8080/index.html"
    webbrowser.open(url)

# if __name__ == "__main__":
#     # Chạy HTTP server trong luồng riêng
#     threading.Thread(target=start_http_server, daemon=True).start()
#
#     # Mở trình duyệt
#     open_browser()
#
#     # Chạy WebSocket server
#     asyncio.run(websocket_server())

