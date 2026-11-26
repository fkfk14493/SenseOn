import asyncio
import threading
import sys
from pathlib import Path

import cv2

from stream_server import update_frame, run_stream_server


# =========================================================
# 프로젝트 경로
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from senseon_pipeline import FrameAnalyzer


# =========================================================
# 설정
# =========================================================

MODEL_PATH = ROOT_DIR / "ai1" / "yolo11n.pt"

# 테스트할 영상 파일 경로
VIDEO_PATH = ROOT_DIR / "test_videos" / "test.mp4"


async def main():
    print("[TEST] AI 모델 로드 시작")

    analyzer = FrameAnalyzer(
        str(MODEL_PATH)
    )

    print("[TEST] AI 모델 로드 완료")


    # =====================================================
    # 스트리밍 서버 시작
    # =====================================================

    stream_thread = threading.Thread(
        target=run_stream_server,
        daemon=True
    )

    stream_thread.start()

    print("[TEST] Live stream server started")


    # =====================================================
    # 영상 열기
    # =====================================================

    cap = cv2.VideoCapture(
        str(VIDEO_PATH)
    )

    if not cap.isOpened():
        print(
            f"[ERROR] 영상 파일을 열 수 없습니다: "
            f"{VIDEO_PATH}"
        )
        return


    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 30.0


    frame_delay = 1.0 / fps

    print(
        f"[TEST] Video FPS: {fps:.2f}"
    )

    print(
        f"[TEST] Video: {VIDEO_PATH}"
    )


    try:
        while True:
            ret, frame = cap.read()

            # =============================================
            # 영상 끝
            # =============================================

            if not ret:
                print(
                    "[TEST] 영상 끝 -> 처음부터 다시 재생"
                )

                cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    0
                )

                continue


            # =============================================
            # 현재 영상 시간
            # =============================================

            timestamp = (
                cap.get(
                    cv2.CAP_PROP_POS_MSEC
                )
                / 1000.0
            )


            # =============================================
            # AI 처리
            # =============================================

            final_result, state, annotated_frame = (
                await asyncio.to_thread(
                    analyzer.process,
                    frame,
                    timestamp,
                    annotate=True
                )
            )


            # =============================================
            # 브라우저 스트림 갱신
            # =============================================

            if annotated_frame is not None:
                update_frame(
                    annotated_frame
                )
            else:
                update_frame(
                    frame
                )


            # =============================================
            # 콘솔 결과
            # =============================================

            if state == "READY":
                print(
                    "[AI] result:",
                    final_result
                )
            else:
                print(
                    f"[AI] state={state}"
                )


            # =============================================
            # 원본 영상 FPS 정도로 재생
            # =============================================

            await asyncio.sleep(
                frame_delay
            )


    except KeyboardInterrupt:
        print()
        print("[TEST] 사용자 종료")


    finally:
        cap.release()

        print(
            "[TEST] Video released"
        )


if __name__ == "__main__":
    asyncio.run(
        main()
    )