# 1. Raspberry Pi 카메라 입력
# 2. AI 코드 통합
# 3. Raspberry Pi -> ESP32 BLE 통신
# 4. 통신 안정성 처리
# 5. End-to-End Latency 측정
# 6. 최종 통합 실행
# 통합 후 camera.py 호출

import asyncio

from mock_ai import get_mock_hazard
from protocol import encode_hazard
from ble_sender import BLESender
from latency import now_ms, calc_latency_ms
from logger import save_log


async def main():
    sender = BLESender()

    try:
        # 1. ESP32 BLE 연결
        await sender.connect_with_retry()

        # 2. AI 결과 받기
        # 현재는 테스트용 Mock AI
        hazard = get_mock_hazard()

        print("AI 결과:", hazard)

        # 3. BLE 전송 패킷 생성
        packet = encode_hazard(hazard)

        print("전송 패킷:", packet)

        # 4. 이전 ACK 상태 초기화
        # 새 패킷의 ACK와 이전 ACK를 구분하기 위함
        sender.clear_ack()

        # 5. AI 판단 완료 시점 기록
        # E2E Latency 측정 시작점
        ai_result_time = now_ms()

        # 6. ESP32로 BLE 전송
        send_success = await sender.send(packet)

        if not send_success:
            print("BLE 전송 실패")
            return

        print("BLE 전송 성공")

        # 7. ESP32가 모터 ON 후 보내는 ACK 대기
        ack_received = await sender.wait_for_ack()

        if not ack_received:
            print("ACK 수신 실패")
            return

        # 8. ACK 수신 시점 기록
        # E2E Latency 측정 종료점
        ack_time = now_ms()

        # 9. End-to-End Latency 계산
        e2e_latency = calc_latency_ms(
            ai_result_time,
            ack_time
        )

        print(
            f"End-to-End Latency: "
            f"{e2e_latency:.3f} ms"
        )

        # 10. 로그 저장
        save_log(
            hazard,
            e2e_latency_ms=e2e_latency
        )

        print("로그 저장 완료")

    finally:
        # 11. BLE 연결 종료
        await sender.disconnect()


if __name__ == "__main__":
    asyncio.run(main())