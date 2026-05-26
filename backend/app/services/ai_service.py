import base64
import os

from openai import OpenAI
from dotenv import load_dotenv


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# OPENAI CLIENT
# =========================

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


# =========================
# ENCODE IMAGE
# =========================

def encode_image(
    image_path
):

    with open(
        image_path,
        "rb"
    ) as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# =========================
# GENERATE VIDEO SUMMARY
# =========================

def generate_video_summary(
    frame_paths,
    transcript
):

    try:

        images = []

        for path in frame_paths[:3]:

            base64_image = encode_image(
                path
            )

            images.append(

                {
                    "type": "image_url",

                    "image_url": {

                        "url":
                        f"data:image/jpeg;base64,{base64_image}"

                    }
                }

            )

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {

                    "role": "user",

                    "content": [

                        {

                            "type": "text",

                            "text":
                            f"""
                            Analyze these video frames
                            and transcript.

                            Transcript:
                            {transcript[:3000]}

                            Generate a concise,
                            clear summary ONLY in English.

                            Even if transcript language
                            is not English,
                            translate and summarize
                            in English.
                            """

                        },

                        *images

                    ]

                }

            ],

            max_tokens=300

        )

        return response.choices[0].message.content

    except Exception as e:

        print(
            f"OpenAI Error: {e}"
        )

        return (
            f"AI summary failed: {str(e)}"
        )

from openai import OpenAI

client = OpenAI()


def summarize_text(text):

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "user",

                    "content":
                    f"""
                    Summarize this video
                    transcript professionally
                    in clear English.

                    Transcript:

                    {text[:5000]}
                    """
                }

            ],

            max_tokens=300

        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return f"Summary error: {e}"