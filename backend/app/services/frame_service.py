import cv2
import os
import shutil


FRAME_DIR = "frames"

os.makedirs(
    FRAME_DIR,
    exist_ok=True
)


def extract_frames(
    video_path,
    video_id,
    interval=3
):

    # =====================
    # UNIQUE VIDEO FOLDER
    # =====================

    video_frame_dir = (
        f"{FRAME_DIR}/{video_id}"
    )

    # =====================
    # REMOVE OLD FRAMES
    # =====================

    if os.path.exists(
        video_frame_dir
    ):

        shutil.rmtree(
            video_frame_dir
        )

    os.makedirs(
        video_frame_dir,
        exist_ok=True
    )

    # =====================
    # VIDEO CAPTURE
    # =====================

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

    # =====================
    # FRAME EXTRACTION
    # =====================

    while True:

        success, frame = cap.read()

        if not success:
            break

        if count % frame_interval == 0:

            frame_path = (
                f"{video_frame_dir}/"
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

    print(
        f"Extracted "
        f"{saved_count} frames"
    )

    return frame_paths