import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime
from config import DEVICE_NAME, CHARACTERISTIC_UUID, RETRY_DELAY


def log(message):
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{now}] {message}")


class BLESender:
    def __init__(self):
        # ESP 정보 불러오기
        self.device_name = DEVICE_NAME
        self.characteristic_uuid = CHARACTERISTIC_UUID

        # ESP32와 연결된 BLE Client 객체를 저장
        # 아직 연결 전이므로 None
        self.client = None


    async def find_device(self):
        # 주변 BLE 장치 중에서
        # ESP32 이름과 같은 장치를 검색
        log(f"[BLE] {self.device_name} 검색 중...")

        # 주변 BLE 장치 검색
        devices = await BleakScanner.discover()

        # 검색된 장치들을 하나씩 확인
        for device in devices:
            if device.name == DEVICE_NAME:
                log(f"[BLE] 장치 발견: {device.name}")

                # 찾은 ESP32 장치 정보 반환
                return device

        # ESP32를 찾지 못한 경우
        log("[BLE] 장치를 찾지 못했습니다.")
        return None


    async def connect(self):
        # 먼저 ESP32 검색
        device = await self.find_device()

        # 검색 실패
        if device is None:
            return False

        # 발견한 ESP32를 대상으로 BLE Client 생성
        self.client = BleakClient(device)

        try:
            # 실제 BLE 연결 시도
            await self.client.connect()

            log("[BLE] 연결 성공")
            return True

        except Exception as e:
            # 연결 중 오류 발생
            log(f"[BLE] 연결 실패: {e}")
            return False

    async def connect_with_retry(self):
        # ==========================================
        # 재연결 로직
        #
        # 연결 실패 시:
        # 3초 대기 → 다시 연결 시도
        # 연결될 때까지 반복
        # ==========================================

        while True:
            if await self.connect():
                return

            log(f"[BLE] {RETRY_DELAY}초 후 재연결")
            await asyncio.sleep(RETRY_DELAY)

    async def send(self, packet):
        # ==========================================
        # 데이터 전송 전에 BLE 연결 상태 확인
        # ==========================================
        
        if not CHARACTERISTIC_UUID:
            raise ValueError("CHARACTERISTIC_UUID가 아직 설정되지 않았습니다.")

        if self.client is None or not self.client.is_connected:
            log("[BLE] 연결 없음. 재연결 시도")
            await self.connect_with_retry()

        try:
            await self.client.write_gatt_char(
                CHARACTERISTIC_UUID,
                packet.encode("utf-8")
            )

            log(f"[BLE] 전송 성공: {packet}")
            return True

        except Exception as e:
            log(f"[BLE] 전송 실패: {e}")
            return False


    async def disconnect(self):
        # 연결되어 있다면 ESP32와 BLE 연결 종료
        if self.client is not None and self.client.is_connected:
            await self.client.disconnect()

            log("[BLE] 연결 종료")