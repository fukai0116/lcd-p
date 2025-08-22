import cv2
from luma.core.interface.serial import spi
from luma.lcd.device import ili9488
from PIL import Image
import time

# --- ここを自分の配線に合わせて設定 ---
SPI_PORT = 0
SPI_DEVICE = 0 # CE0 を使う場合
GPIO_DC = 24
GPIO_RST = 25
# -----------------------------------

# SPIインターフェースをセットアップ
# bus_speed_hz は環境によって調整（高すぎると不安定になる場合がある）
serial = spi(port=SPI_PORT, device=SPI_DEVICE, gpio_DC=GPIO_DC, gpio_RST=GPIO_RST, bus_speed_hz=32000000)

# ILI9488デバイスをセットアップ
device = ili9488(serial, active_low=False, width=480, height=320)

# USBカメラを初期化 (0は通常、内蔵 or 最初に見つかったUSBカメラ)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("エラー: USBカメラを開けません。")
    exit()

print("カメラ映像の表示を開始します。終了するには Ctrl+C を押してください。")

try:
    while True:
        # カメラから1フレーム読み込む
        ret, frame = cap.read()
        if not ret:
            print("フレームを読み込めませんでした。")
            time.sleep(1)
            continue

        # OpenCVの画像形式(BGR)からPillowで扱える形式(RGB)に変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        # 液晶の解像度に合わせて画像をリサイズ
        resized_image = pil_image.resize(device.size)

        # 液晶に画像を表示
        device.display(resized_image)

except KeyboardInterrupt:
    print("プログラムを終了します。")
finally:
    # 後片付け
    cap.release()
    device.cleanup()

