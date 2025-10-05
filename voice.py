import requests
from config import ELEVEN_API_KEY, ELEVEN_API_URL

headers = {
    "xi-api-key": ELEVEN_API_KEY
}


def get_voices() -> dict:
    """
    Получение списка доступных голосов
    """
    url = f"{ELEVEN_API_URL}/voices"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    voices = {voice["name"]: voice["voice_id"] for voice in data["voices"]}
    return voices


def text_to_speech(text: str, voice_id: str) -> bytes:
    """
    Генерация озвучки через ElevenLabs
    """
    url = f"{ELEVEN_API_URL}/text-to-speech/{voice_id}"
    headers_post = {
        "xi-api-key": ELEVEN_API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers_post, json=payload)
    response.raise_for_status()
    return response.content