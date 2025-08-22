import cv2
from luma.core.interface.serial import spi
from luma.lcd.device import ili9488
from PIL import Image
import time

# --- ピン設定（ご自身の配線に合わせてください） ---
SPI_PORT = 0
SPI_DEVICE = 0
GPIO_DC = 24
GPIO_RST = 25
# -----------------------------------

print("1. ライブラリのインポート完了")

# SPIとデバイスをセットアップ
try:
    serial = spi(port=SPI_PORT, device=SPI_DEVICE, gpio_DC=GPIO_DC, gpio_RST=GPIO_RST, bus_speed_hz=32000000)
    device = ili9488(serial, active_low=False, width=480, height=320)
    print("2. 液晶デバイスの初期化完了")
except Exception as e:
    print(f"液晶の初期化でエラー: {e}")
    exit()

# カメラを初期化
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("エラー: USBカメラを開けません。")
    exit()

print("3. カメラの初期化完了、映像ループを開始します...")
frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームを読み込めませんでした。")
            time.sleep(1)
            continue
        
        # 10フレームごとに進捗を表示
        if frame_count % 10 == 0:
            print(f"フレーム {frame_count} を処理中...")

        # 画像を変換してリサイズ
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        resized_image = pil_image.resize(device.size)

        # 液晶に表示
        device.display(resized_image)
        
        frame_count += 1

except KeyboardInterrupt:
    print("プログラムを終了します。")
finally:
    cap.release()
    device.cleanup()