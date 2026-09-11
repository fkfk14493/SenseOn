import asyncio
from bleak import BleakClient, BleakScanner


class BLESender:
    def __init__(self, device_name, characteristic_uuid):
        # =========================================
        # ESP32 BLE 정보
        # =========================================
        # device_name:
        #   ESP32에서 설정한 BLE 장치 이름
        #   예: "SenseOn_ESP32"
        #
        # characteristic_uuid:
        #   ESP32에서 데이터를 수신하도록 만든
        #   BLE Characteristic의 UUID
        #
        # ※ 실제 ESP32 코드가 완성되면
        #   ESP32 담당자에게 이 두 값을 받아서 넣으면 됨.
        # =========================================
        self.device_name = device_name
        self.characteristic_uuid = characteristic_uuid

        # ESP32와 연결된 BLE Client 객체를 저장
        # 아직 연결 전이므로 None
        self.client = None


    async def find_device(self):
        # 주변 BLE 장치 중에서
        # ESP32 이름과 같은 장치를 검색
        print(f"[BLE] {self.device_name} 검색 중...")

        # 주변 BLE 장치 검색
        devices = await BleakScanner.discover()

        # 검색된 장치들을 하나씩 확인
        for device in devices:
            if device.name == self.device_name:
                print(f"[BLE] 장치 발견: {device.name}")

                # 찾은 ESP32 장치 정보 반환
                return device

        # ESP32를 찾지 못한 경우
        print("[BLE] 장치를 찾지 못했습니다.")
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

            print("[BLE] 연결 성공")
            return True

        except Exception as e:
            # 연결 중 오류 발생
            print(f"[BLE] 연결 실패: {e}")
            return False

    async def connect_with_retry(self, retry_delay=3):
        # ==========================================
        # 재연결 로직
        #
        # 연결 실패 시:
        # 3초 대기 → 다시 연결 시도
        # 연결될 때까지 반복
        # ==========================================

        while True:
            connected = await self.connect()

            if connected:
                return True

            print(f"[BLE] {retry_delay}초 후 다시 연결합니다.")
            await asyncio.sleep(retry_delay)

    async def send(self, packet):
        # ==========================================
        # 데이터 전송 전에 BLE 연결 상태 확인
        # ==========================================

        if self.client is None or not self.client.is_connected:
            print("[BLE] 연결이 끊어졌습니다. 재연결을 시도합니다.")

            # 자동 재연결
            await self.connect_with_retry()

        # ESP32와 연결되어 있는지 확인
        if self.client is None or not self.client.is_connected:
            print("[BLE] 연결되어 있지 않습니다.")
            return False

        try:
            # =========================================
            # ESP32로 실제 데이터를 보내는 부분
            # =========================================
            #
            # self.characteristic_uuid:
            #   ESP32의 수신용 Characteristic UUID
            #
            # packet:
            #   예: "car,LEFT,DANGER,1.8"
            #
            # encode("utf-8"):
            #   문자열을 BLE로 보낼 수 있도록 bytes로 변환
            # =========================================
            await self.client.write_gatt_char(
                self.characteristic_uuid,
                packet.encode("utf-8")
            )

            print(f"[BLE] 전송: {packet}")
            return True

        except Exception as e:
            print(f"[BLE] 전송 실패: {e}")
            return False


    async def disconnect(self):
        # 연결되어 있다면 ESP32와 BLE 연결 종료
        if self.client is not None and self.client.is_connected:
            await self.client.disconnect()

            print("[BLE] 연결 종료")