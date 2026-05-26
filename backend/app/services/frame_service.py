import cv2
import os


FRAME_DIR = "frames"

os.makedirs(
    FRAME_DIR,
    exist_ok=True
)


def extract_frames(
    video_path,
    interval=3
):

    frame_paths = []

    cap = cv2.VideoCapture(
        video_path
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps == 0:

        fps = 30

    frame_interval = int(
        fps * interval
    )

    count = 0

    saved_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        if count % frame_interval == 0:

            frame_path = (
                f"{FRAME_DIR}/"
                f"frame_{saved_count}.jpg"
            )

            cv2.imwrite(
                frame_path,
                frame
            )

            frame_paths.append(
                frame_path
            )

            saved_count += 1

        count += 1

    cap.release()

    return frame_paths