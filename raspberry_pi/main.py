# 1. Raspberry Pi 
# 2. AI 
# 3. Raspberry Pi -> ESP32 BLE
# 4. 
# 5. End-to-End Latency
# 6. 

from mock_ai import get_mock_hazard
from protocol import encode_hazard
from ble_sender import BLESender

print("ble_sender import 성공")

sender = BLESender(
    device_name="SenseOn_ESP32",
    characteristic_uuid="12345678-1234-5678-1234-56789abcdef0"
)

print("BLESender 생성 성공")
print(sender.device_name)
print(sender.characteristic_uuid)


def main():
    hazard = get_mock_hazard()
    packet = encode_hazard(hazard)

    print("AI 결과:", hazard)
    print("전송 패킷:", packet)


if __name__ == "__main__":
    main()