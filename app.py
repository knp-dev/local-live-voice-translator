import sys
import argparse
from numpy.typing import NDArray
from fastrtc import (
    ReplyOnPause,
    Stream
)
from core.faster_whisper import FasterWhisperSTT
from core.handler import init_lang_handler, lang_dict
from core.kokoro import (
    CustomKokoroTTSOptions,
    CustomKokoroTTSModel
)
from loguru import logger
from ollama import chat

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

def echo(audio: tuple[int, NDArray]):
    segments,_ = stt_model.stt(audio)
    transcript = " ".join(segment.text for segment in segments).strip()
    logger.debug(f"🎤 Transcript: {transcript}")
    response_text = transcript
    # Don't translate if the source and target language are the same
    if _.language not in voice_options.lang:
        target_language = lang_handler.full
        system_prompt = f"""
        You are an expert in {", ".join(lang_dict.values())} and {target_language}.
        Please provide a high-quality translation of the following text to {target_language}.
        Only generate the translated text. No additional text or explanation needed.
        """
        response = chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": transcript},
            ],
            options={"num_predict": 200},
        )
        response_text = response["message"]["content"]
        logger.debug(f"🤖 Response: {response_text}")
    if use_voice:
        response_text = lang_handler.process(response_text)
        for audio_chunk in tts_model.stream_tts_sync(response_text, voice_options):
            yield audio_chunk
    else:
        yield

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local Live Voice Translator")
    parser.add_argument("--novoice", action="store_true", help="Launch without voice", default=False)
    parser.add_argument('-port', action="store", type=int, help="UI Port", default=7860)
    parser.add_argument('-lang', action="store", type=str, help="Target Language [en|es|fr|hi|it|ja|ptbr|zh]", default='en')
    args = parser.parse_args()

    use_voice = not args.novoice
    if use_voice:
        # Init kokoro
        tts_model = CustomKokoroTTSModel()
        tts_model.tts("Hello World!")

    # stt_model = get_stt_model()  # moonshine/base
    stt_model = FasterWhisperSTT()
    lang_handler = init_lang_handler(args.lang)
    voice_options = CustomKokoroTTSOptions(lang=lang_handler.short,
                                    voice=lang_handler.voice,
                                    is_phonemes=lang_handler.is_phonemes)

    stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
    stream.ui.launch(server_port=args.port)