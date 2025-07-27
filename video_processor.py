# video_processor.py
from gtts import gTTS
import requests
import os
import tempfile
from pexels_api import API

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")  # hoặc dùng streamlit.secrets nếu tích hợp streamlit

def process_video(text_chunk, index, keyword="sky"):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Lấy ảnh
        pexels_api = API(PEXELS_API_KEY)
        pexels_api.search(keyword, page=1, results_per_page=1)
        photo_url = pexels_api.get_entries()[0].original
        image_path = os.path.join(tmpdir, f"image_{index}.jpg")
        with open(image_path, 'wb') as f:
            f.write(requests.get(photo_url).content)

        # TTS
        tts = gTTS(text_chunk, lang='vi')
        audio_path = os.path.join(tmpdir, f"audio_{index}.mp3")
        tts.save(audio_path)

        # Ghép
        clip = ImageClip(image_path, duration=10).set_audio(AudioFileClip(audio_path))
        clip = clip.set_duration(clip.audio.duration)
        output_path = os.path.join(tmpdir, f"video_{index}.mp4")
        clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

        return output_path
