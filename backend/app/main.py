from fastapi import (
    FastAPI,
    UploadFile,
    File,
    BackgroundTasks
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.services.frame_service import (
    extract_frames
)

from app.services.ai_service import (
    generate_video_summary
)

from app.services.audio_service import (
    transcribe_video
)

from app.services.youtube_service import (
    get_youtube_transcript
)

from app.services.ai_service import (
    summarize_text
)

from fastapi.staticfiles import (
    StaticFiles
)

import shutil
import os
import uuid


app = FastAPI()

app.mount(
    "/frames",
    StaticFiles(directory="frames"),
    name="frames"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# DIRECTORIES
# =========================

UPLOAD_DIR = "uploads"

OUTPUT_DIR = "output"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =========================
# IN-MEMORY STATUS STORE
# =========================

video_results = {}


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "AI Video Summarizer Running"
    }


# =========================
# BACKGROUND PROCESSING
# =========================

def process_video(
    video_id,
    video_path
):

    try:

        print(
            f"Started processing: {video_path}"
        )

        # =====================
        # PROCESSING START
        # =====================

        video_results[video_id] = {

            "status": "processing",

            "progress": 10

        }

        # =====================
        # FRAME EXTRACTION
        # =====================

        video_results[video_id] = {

            "status": "extracting_frames",

            "progress": 30

        }

        frame_paths = extract_frames(
            video_path
        )

        # =====================
        # AUDIO TRANSCRIPTION
        # =====================

        video_results[video_id] = {

            "status": "transcribing_audio",

            "progress": 60

        }

        transcript = transcribe_video(
            video_path
        )

        # =====================
        # AI SUMMARY
        # =====================

        video_results[video_id] = {

            "status": "analyzing_video",

            "progress": 85

        }

        ai_summary = generate_video_summary(
            frame_paths,
            transcript
        )

        # =====================
        # FRAMES EXTRACTED
        # =====================

        video_results[video_id] = {

            "status": "frames_extracted",

            "progress": 70

        }

        # =====================
        # FINAL RESULT
        # =====================

        video_results[video_id] = {

            "status": "completed",

            "progress": 100,

            "summary":
                ai_summary,

            "video_path":
                video_path,

            "total_frames":
                len(frame_paths),

            "frames":
                frame_paths[:10],

            "transcript":
                transcript[:1000],

        }

        print(
            f"Completed: {video_id}"
        )

    except Exception as e:

        print(
            f"Processing error: {e}"
        )

        video_results[video_id] = {

            "status": "failed",

            "error": str(e)

        }


# =========================
# VIDEO UPLOAD
# =========================

@app.post("/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):

    try:

        # =====================
        # FILE SIZE CHECK
        # =====================

        MAX_FILE_SIZE = (
            5 * 1024 * 1024 * 1024
        )  # 5GB

        file.file.seek(0, 2)

        file_size = file.file.tell()

        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:

            return {

                "success": False,

                "message":
                    "Video exceeds 5GB limit."

            }

        # =====================
        # UNIQUE VIDEO ID
        # =====================

        video_id = str(
            uuid.uuid4()
        )

        safe_filename = (
            file.filename.replace(
                " ",
                "_"
            )
        )

        file_path = (
            f"{UPLOAD_DIR}/"
            f"{video_id}_{safe_filename}"
        )

        # =====================
        # SAVE FILE
        # =====================

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # =====================
        # INITIAL STATUS
        # =====================

        video_results[video_id] = {

            "status": "uploaded",

            "progress": 0

        }

        # =====================
        # BACKGROUND TASK
        # =====================

        background_tasks.add_task(
            process_video,
            video_id,
            file_path
        )

        return {

            "success": True,

            "video_id": video_id,

            "message":
                "Upload successful. "
                "Processing started."

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }


@app.post("/youtube")
async def youtube_summary(
    data: dict
):

    try:

        url = data.get("url")

        if not url:

            return {

                "success": False,

                "message":
                "No URL provided."

            }

        transcript = get_youtube_transcript(
            url
        )

        if not transcript:

            return {

                "success": False,

                "message":
                "Transcript unavailable."

            }

        summary = summarize_text(
            transcript
        )

        return {

            "success": True,

            "summary": summary,

            "transcript":
                transcript[:3000]

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }

# =========================
# STATUS ENDPOINT
# =========================

@app.get("/status/{video_id}")
async def get_status(
    video_id: str
):

    if video_id not in video_results:

        return {

            "status": "not_found"

        }

    return video_results[video_id]