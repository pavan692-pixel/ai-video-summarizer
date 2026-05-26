import { useState } from "react";

import { useDropzone } from "react-dropzone";


function App() {

  const [video, setVideo] = useState(null);

  const [loading, setLoading] = useState(false);

  const [progress, setProgress] = useState(0);

  const [status, setStatus] = useState("");

  const [summary, setSummary] = useState("");

  const [transcript, setTranscript] = useState("");

  const [frames, setFrames] = useState([]);

  const [youtubeUrl, setYoutubeUrl] = useState("");

  const BACKEND_URL =
    "https://supreme-telegram-ww4qp9jrg7qh97gj-8000.app.github.dev";


  // =========================
  // DRAG & DROP
  // =========================

  const onDrop = (acceptedFiles) => {

    if (acceptedFiles.length > 0) {

      setVideo(
        acceptedFiles[0]
      );

      setYoutubeUrl("");

    }

  };

  const {

    getRootProps,

    getInputProps,

    isDragActive

  } = useDropzone({

    onDrop,

    accept: {

      "video/*": []

    }

  });


  // =========================
  // POLLING
  // =========================

  const pollStatus = async (
    videoId
  ) => {

    const interval = setInterval(
      async () => {

        try {

          const response = await fetch(
            `${BACKEND_URL}/status/${videoId}`
          );

          const data =
            await response.json();

          console.log(data);

          setProgress(
            data.progress || 0
          );

          setStatus(
            data.status || ""
          );

          if (
            data.status ===
            "completed"
          ) {

            clearInterval(interval);

            setLoading(false);

            setSummary(
              data.summary || ""
            );

            setTranscript(
              data.transcript || ""
            );

            setFrames(
              data.frames || []
            );

          }

          if (
            data.status ===
            "failed"
          ) {

            clearInterval(interval);

            setLoading(false);

            alert(
              "Processing failed."
            );

          }

        } catch (error) {

          console.error(error);

          clearInterval(interval);

          setLoading(false);

        }

      },

      2000
    );
  };


  // =========================
  // HANDLE UPLOAD
  // =========================

  const handleUpload = async () => {

    if (
      !video &&
      !youtubeUrl
    ) {

      alert(
        "Upload a video or paste YouTube URL."
      );

      return;

    }

    try {

      setLoading(true);

      setSummary("");

      setTranscript("");

      setFrames([]);

      setProgress(0);

      setStatus("uploading");

      let response;


      // =========================
      // YOUTUBE MODE
      // =========================

      if (youtubeUrl) {

        response = await fetch(
          `${BACKEND_URL}/youtube`,
          {

            method: "POST",

            headers: {

              "Content-Type":
              "application/json"

            },

            body: JSON.stringify({

              url: youtubeUrl

            })

          }
        );

        const data =
          await response.json();

        console.log(data);

        if (data.success) {

          setSummary(
            data.summary || ""
          );

          setTranscript(
            data.transcript || ""
          );

          setFrames(
            data.frames || []
          );

        } else {

          alert(
            data.message ||
            "YouTube processing failed."
          );

        }

        setLoading(false);

        return;

      }


      // =========================
      // VIDEO UPLOAD MODE
      // =========================

      const formData =
        new FormData();

      formData.append(
        "file",
        video
      );

      response = await fetch(
        `${BACKEND_URL}/upload`,
        {

          method: "POST",

          body: formData,

        }
      );

      const data =
        await response.json();

      console.log(data);

      if (data.success) {

        pollStatus(
          data.video_id
        );

      } else {

        setLoading(false);

        alert(
          data.message ||
          "Upload failed."
        );

      }

    } catch (error) {

      console.error(error);

      setLoading(false);

      alert(
        "Something went wrong."
      );

    }

  };


  return (

    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">

      <div className="max-w-5xl mx-auto">


        {/* ========================= */}
        {/* HEADER */}
        {/* ========================= */}

        <div className="text-center mb-12">

          <h1 className="text-5xl font-bold mb-4">

            AI Video Summarizer

          </h1>

          <p className="text-slate-400 text-lg">

            Upload videos or paste YouTube links
            to generate AI-powered summaries.

          </p>

        </div>


        {/* ========================= */}
        {/* MAIN BOX */}
        {/* ========================= */}

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">


          {/* ========================= */}
          {/* YOUTUBE INPUT */}
          {/* ========================= */}

          <div className="mb-6">

            <input
              type="text"
              placeholder="Paste YouTube URL"
              value={youtubeUrl}
              onChange={(e) =>
                setYoutubeUrl(
                  e.target.value
                )
              }
              className="
                w-full
                bg-slate-800
                border
                border-slate-700
                rounded-2xl
                p-4
                text-white
                outline-none
              "
            />

          </div>


          {/* ========================= */}
          {/* OR TEXT */}
          {/* ========================= */}

          <div className="text-center text-slate-500 mb-6">

            OR

          </div>


          {/* ========================= */}
          {/* DRAG DROP */}
          {/* ========================= */}

          <div
            {...getRootProps()}
            className={`
              border-2
              border-dashed
              rounded-2xl
              p-14
              text-center
              cursor-pointer
              transition-all
              duration-300

              ${
                isDragActive
                  ? "border-blue-500 bg-slate-800"
                  : "border-slate-600 hover:border-blue-500"
              }
            `}
          >

            <input {...getInputProps()} />

            {

              isDragActive ?

              (

                <p className="text-xl">

                  Drop video here...

                </p>

              )

              :

              (

                <div>

                  <p className="text-2xl font-semibold mb-3">

                    Drag & Drop Video

                  </p>

                  <p className="text-slate-400">

                    or click to browse

                  </p>

                </div>

              )

            }

          </div>


          {/* ========================= */}
          {/* FILE NAME */}
          {/* ========================= */}

          {video && (

            <div className="mt-5 text-center">

              <p className="text-green-400">

                Selected:
                {" "}
                {video.name}

              </p>

            </div>

          )}


          {/* ========================= */}
          {/* BUTTON */}
          {/* ========================= */}

          <div className="mt-8 text-center">

            <button
              onClick={handleUpload}
              disabled={loading}
              className="
                bg-blue-600
                hover:bg-blue-700
                px-8
                py-4
                rounded-2xl
                text-lg
                font-semibold
                transition
                disabled:opacity-50
              "
            >

              {

                loading ?

                "Processing..."

                :

                "Generate Summary"

              }

            </button>

          </div>


          {/* ========================= */}
          {/* LOADING */}
          {/* ========================= */}

          {loading && (

            <div className="mt-8">

              <div className="w-full bg-slate-700 rounded-full h-5 overflow-hidden">

                <div
                  className="
                    bg-blue-500
                    h-5
                    rounded-full
                    transition-all
                    duration-500
                  "
                  style={{
                    width: `${progress}%`
                  }}
                />

              </div>

              <div className="flex justify-between mt-3">

                <p className="capitalize text-slate-300">

                  {status}

                </p>

                <p className="text-slate-300">

                  {progress}%

                </p>

              </div>

            </div>

          )}

        </div>


        {/* ========================= */}
        {/* SUMMARY */}
        {/* ========================= */}

        {summary && (

          <div className="mt-10 bg-slate-900 border border-slate-800 rounded-3xl p-8">

            <h2 className="text-3xl font-bold mb-5">

              AI Summary

            </h2>

            <p className="leading-8 text-slate-200 whitespace-pre-wrap">

              {summary}

            </p>

          </div>

        )}


        {/* ========================= */}
        {/* TRANSCRIPT */}
        {/* ========================= */}

        {transcript && (

          <div className="mt-10 bg-slate-900 border border-slate-800 rounded-3xl p-8">

            <h2 className="text-3xl font-bold mb-5">

              Transcript

            </h2>

            <p className="leading-7 text-sm text-slate-300 whitespace-pre-wrap">

              {transcript}

            </p>

          </div>

        )}


        {/* ========================= */}
        {/* FRAMES */}
        {/* ========================= */}

        {frames.length > 0 && (

          <div className="mt-10">

            <h2 className="text-3xl font-bold mb-6">

              Extracted Frames

            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

              {frames.map(
                (
                  frame,
                  index
                ) => (

                  <img
                    key={index}
                    src={`${BACKEND_URL}/${frame}`}
                    alt={`frame-${index}`}
                    className="
                      rounded-2xl
                      border
                      border-slate-700
                      shadow-lg
                    "
                  />

                )
              )}

            </div>

          </div>

        )}

      </div>

    </div>

  );
}

export default App;