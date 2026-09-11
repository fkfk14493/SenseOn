# 1. Raspberry Pi 카메라 입력
# 2. AI 코드 통합
# 3. Raspberry Pi -> ESP32 BLE 통신
# 4. 통신 안정성 처리
# 5. End-to-End Latency 측정
# 6. 최종 통합 실행

from mock_ai import get_mock_hazard
from protocol import encode_hazard
from ble_sender import BLESender
from latency import now_ms, calc_latency_ms
from logger import save_log

sender = BLESender(
    device_name="SenseOn_ESP32",
    characteristic_uuid="12345678-1234-5678-1234-56789abcdef0"
)

print("BLESender 생성 성공")
print(sender.device_name)
print(sender.characteristic_uuid)


def main():
    # AI 결과가 만들어졌다고 가정하는 시점
    ai_result_time = now_ms()

    hazard = get_mock_hazard()
    packet = encode_hazard(hazard)

    # BLE로 보내기 직전 시점
    ble_send_time = now_ms()

    latency = calc_latency_ms(ai_result_time, ble_send_time)

    print("AI 결과:", hazard)
    print("전송 패킷:", packet)
    print(f"AI 결과 → BLE 송신 준비 지연시간: {latency:.3f} ms")

    # CSV 파일에 결과 저장
    save_log(hazard, ble_latency_ms=latency)
    print("로그 저장 완료")

if __name__ == "__main__":
    main()