from youtube_transcript_api import (
    YouTubeTranscriptApi
)

import re


def extract_video_id(url):

    regex = (
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    )

    match = re.search(
        regex,
        url
    )

    if match:

        return match.group(1)

    return None


def get_youtube_transcript(url):

    try:

        video_id = extract_video_id(
            url
        )

        if not video_id:

            return None

        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id
        )

        text = " ".join([

            item.text

            for item in transcript

        ])

        return text

    except Exception as e:

        print(
            f"YouTube Transcript Error: {e}"
        )

        return None