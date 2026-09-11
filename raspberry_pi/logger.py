import csv
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "senseon_log.csv")


def save_log(hazard, ble_latency_ms=None):
    # 파일이 처음 만들어지는지 확인
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # 파일이 처음 생성될 때 헤더 작성
        if not file_exists:
            writer.writerow([
                "timestamp",
                "object",
                "direction",
                "risk",
                "ttc",
                "ble_latency_ms"
            ])

        # 실제 데이터 저장
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            hazard["object"],
            hazard["direction"],
            hazard["risk"],
            hazard["ttc"],
            ble_latency_ms
        ])