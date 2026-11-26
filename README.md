# SenseOn — Raspberry Pi 기반 후방 충돌위험 감지 시스템

2026 제5회 전공융합 프로젝트 대회(MEIT) | Team SenseOn

본 저장소는 팀 프로젝트 중 **Raspberry Pi 5 측 소프트웨어 구현 코드**를 정리한 것입니다.

## 1. 프로젝트 소개

SenseOn은 후방에서 접근하는 이동수단을 AI로 탐지·추적하고, 위험 상황을 진동 및 디스플레이로 알려주는 웨어러블 경고 시스템입니다.

**전체 시스템 구조**

Camera → Raspberry Pi 5 → BLE → ESP32 → 진동 모터·OLED

- 객체 탐지: YOLO11n
- 객체 추적: BoT-SORT
- 위험 판단: 접근 방향, 이동 궤적, TTC 등을 활용한 위험 단계 분류

## 2. 담당 구현 기능

**Raspberry Pi 5 기반 소프트웨어 통합 및 통신 기능 구현**

- **시스템 통합:** Linux 환경에서 카메라 입력, 기존 AI 인지 파이프라인, BLE 통신 모듈 연동
- **실시간 스트리밍:** Flask·OpenCV 기반 MJPEG 스트리밍으로 객체 탐지 결과를 웹브라우저에 출력
- **BLE 통신:** Bleak을 활용한 ESP32 연결, 위험정보 패킷 전송, ACK 수신 및 재연결 처리
- **성능 측정:** AI 판단 완료부터 ESP32 ACK 수신까지의 지연시간 측정 및 CSV 로그 기록
- **기능 테스트:** 카메라 입력, BLE 송수신, 저장 영상 기반 스트리밍 테스트 코드 작성

※ AI 모델 학습·위험 판단 알고리즘과 ESP32 측 제어 코드는 팀 내 다른 구현 영역으로, 본 저장소에는 포함되어 있지 않습니다.

## 3. 개발 환경

| 구분 | 기술 |
|---|---|
| Hardware | Raspberry Pi 5, Camera, ESP32 |
| Language | Python |
| OS | Linux |
| Libraries | Picamera2, Flask, OpenCV, Bleak |
| Communication | BLE |

현재 저장소는 Raspberry Pi 측 구현 코드를 중심으로 공개하며, 외부 AI 파이프라인 및 모델 파일이 포함되지 않아 전체 시스템의 단독 실행은 지원하지 않습니다.

## 4. 결과 및 동작 영상

**팀 전체 시스템 성능 평가 결과**

| 평가 지표 | 결과 |
|---|---:|
| 오경보율 | 16.1% |
| 위험 감지율 | 71.4% |
| 평균 응답 지연 | 125.1 ms |
| 처리 FPS | 9.76~11.35 FPS |

평균 응답 지연은 AI 판단 완료부터 ESP32 ACK 수신까지의 시간입니다.

### 동작 영상

https://github.com/user-attachments/assets/951a9bde-6222-44af-9fdb-789d84233279

