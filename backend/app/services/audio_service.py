import whisper


# =========================
# LOAD MODEL
# =========================

model = whisper.load_model(
    "base"
)


# =========================
# TRANSCRIBE VIDEO
# =========================

def transcribe_video(
    video_path
):

    try:

        result = model.transcribe(
            video_path
        )

        transcript = result["text"]

        if transcript.strip() == "":

            return (
                "No speech detected."
            )

        return transcript

    except Exception as e:

        print(
            f"Whisper error: {e}"
        )

        return (
            "Audio transcription failed."
        )