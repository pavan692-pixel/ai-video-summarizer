import os
import re
import time
import requests

from youtube_transcript_api import (
    YouTubeTranscriptApi
)


# =========================
# CACHE DIRECTORY
# =========================

CACHE_DIR = "cache"

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)


# =========================
# WEBSHARE PROXY
# =========================

WEBSHARE_USERNAME = os.getenv(
    "WEBSHARE_USERNAME"
)

WEBSHARE_PASSWORD = os.getenv(
    "WEBSHARE_PASSWORD"
)

PROXY_URL = (
    f"http://{WEBSHARE_USERNAME}:"
    f"{WEBSHARE_PASSWORD}"
    f"@p.webshare.io:9999"
)


# =========================
# CREATE SESSION
# =========================

def create_proxy_session():

    session = requests.Session()

    session.proxies.update({

        "http": PROXY_URL,

        "https": PROXY_URL,

    })

    return session


# =========================
# EXTRACT VIDEO ID
# =========================

def extract_video_id(url):

    regex = (
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    )

    match = re.search(
        regex,
        url
    )

    return (
        match.group(1)
        if match else None
    )


# =========================
# CACHE PATH
# =========================

def get_cache_path(video_id):

    return (
        f"{CACHE_DIR}/{video_id}.txt"
    )


# =========================
# LOAD CACHE
# =========================

def load_cached_transcript(
    video_id
):

    cache_path = get_cache_path(
        video_id
    )

    if os.path.exists(cache_path):

        with open(
            cache_path,
            "r",
            encoding="utf-8"
        ) as f:

            print(
                "Transcript loaded from cache"
            )

            return f.read()

    return None


# =========================
# SAVE CACHE
# =========================

def save_transcript_cache(
    video_id,
    transcript
):

    cache_path = get_cache_path(
        video_id
    )

    with open(
        cache_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(transcript)

    print(
        "Transcript cached successfully"
    )


# =========================
# GET TRANSCRIPT
# =========================

def get_youtube_transcript(url):

    try:

        # =====================
        # EXTRACT VIDEO ID
        # =====================

        video_id = extract_video_id(
            url
        )

        if not video_id:

            print(
                "Invalid YouTube URL"
            )

            return None

        # =====================
        # CHECK CACHE
        # =====================

        cached_transcript = (
            load_cached_transcript(
                video_id
            )
        )

        if cached_transcript:

            return cached_transcript

        # =====================
        # FETCH TRANSCRIPT
        # =====================

        retries = 3

        for attempt in range(retries):

            try:

                print(
                    f"Fetching transcript "
                    f"(Attempt {attempt+1})"
                )

                session = (
                    create_proxy_session()
                )

                ytt_api = (
                    YouTubeTranscriptApi(
                        http_client=session
                    )
                )

                # =================
                # GET TRANSCRIPT
                # =================

                transcript_list = (
                    ytt_api.list(video_id)
                )

                transcript = None

                # =================
                # TRY ENGLISH
                # =================

                try:

                    transcript = (
                        transcript_list
                        .find_transcript(
                            ["en"]
                        )
                        .fetch()
                    )

                    print(
                        "Using English transcript"
                    )

                # =================
                # TRY GENERATED
                # =================

                except:

                    try:

                        transcript = (
                            transcript_list
                            .find_generated_transcript(
                                ["hi", "en"]
                            )
                            .fetch()
                        )

                        print(
                            "Using generated transcript"
                        )

                    # =================
                    # FALLBACK
                    # =================

                    except:

                        available = list(
                            transcript_list
                        )

                        transcript = (
                            available[0]
                            .fetch()
                        )

                        print(
                            "Using fallback transcript"
                        )

                # =================
                # CONVERT TO TEXT
                # =================

                text = " ".join([

                    item.text

                    for item in transcript

                ])

                # =================
                # SAVE CACHE
                # =================

                save_transcript_cache(
                    video_id,
                    text
                )

                print(
                    "Transcript fetched successfully"
                )

                return text

            except Exception as e:

                print(
                    f"Retry {attempt+1}: {e}"
                )

                time.sleep(3)

        print(
            "Failed after retries"
        )

        return None

    except Exception as e:

        print(
            "Transcript Error:",
            e
        )

        return None