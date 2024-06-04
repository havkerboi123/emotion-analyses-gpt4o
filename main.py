



# %pip install --upgrade openai --quiet
# %pip install opencv-python --quiet
# %pip install moviepy --quiet

from openai import OpenAI
import os

model = "gpt-4o"
api_key = "key-here"

client = OpenAI(api_key=api_key)

import cv2
from moviepy.editor import VideoFileClip
import time
import base64

VIDEO_PATH = "/content/vid2.mp4"



def process_video(video_path, seconds_per_frame=2):
    base64Frames = []
    base_video_path, _ = os.path.splitext(video_path)

    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frames_to_skip = int(fps * seconds_per_frame)
    curr_frame=0

    while curr_frame < total_frames - 1:
        video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
        curr_frame += frames_to_skip
    video.release()

    #Extracting audio from video
    audio_path = f"{base_video_path}.mp3"
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, bitrate="32k")
    clip.audio.close()
    clip.close()

    print(f"Extracted {len(base64Frames)} frames")
    print(f"Extracted audio to {audio_path}")
    return base64Frames, audio_path

# Extract 1 frame per second. You can adjust the `seconds_per_frame` parameter to change the sampling rate
base64Frames, audio_path = process_video(VIDEO_PATH, seconds_per_frame=1)

from openai import OpenAI


api_key = "

client = OpenAI(api_key=api_key)

audio_file = open("vid2.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are analyzing video frames and audio to predict the human emotion conveyed by the individual. Respond accordingly."},
        {"role": "user", "content": [
            "These are the frames from the video.",
            *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames),
            {"type": "text", "text": f"The audio transcription is: {transcription.text}"}
        ]}
    ],
    temperature=0,
)

# Print the response content
summary=response.choices[0].message.content

