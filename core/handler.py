from dataclasses import dataclass
from types import MethodType
from misaki import ja, zh

lang_dict = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "ptbr": "Brazilian Portuguese",
    "zh": "Chinese"
}

@dataclass
class LangHandler():
    short: str = "en-us"
    full: str = lang_dict['en']
    voice: str = "af_bella"
    is_phonemes: bool = False
    def process(self, x: str) -> str: return x

def init_lang_handler(lang):
    if (lang == 'en'):
        lang_handler = LangHandler()
    elif (lang == 'en-gb'):
        # British English (bf_alice)
        lang_handler = LangHandler(short="en-gb", voice="bf_alice")
    elif (lang == 'es'):
        # Spanish (ef_dora)
        lang_handler = LangHandler(short="es", full=lang_dict[lang], voice="ef_dora")
    elif (lang == 'fr'):
        # French (ff_siwis)
        lang_handler = LangHandler(short="fr-fr", full=lang_dict[lang], voice="ff_siwis")
    elif (lang == 'hi'):
        # Hindi (hf_alpha)
        lang_handler = LangHandler(short="hi", full=lang_dict[lang], voice="hf_alpha")
    elif (lang == 'it'):
        # Italian (if_sara)
        lang_handler = LangHandler(short="it", full=lang_dict[lang], voice="if_sara")
    elif (lang == 'ja'):
        # Japanese (jf_alpha)
        lang_handler = LangHandler(short="ja", full=lang_dict[lang], voice="jf_alpha", is_phonemes=True)
        lang_handler.process = MethodType(lambda self, x: ja.JAG2P()(x)[0], lang_handler)
    elif (lang == 'ptbr'):
        # Brazilian Portuguese (pf_dora)
        lang_handler = LangHandler(short="pt-br", full=lang_dict[lang], voice="pf_dora")
    elif (lang == 'zh'):
        # Chinese (zf_xiaobei)
        lang_handler = LangHandler(short="zh", full=lang_dict[lang], voice="zf_xiaobei", is_phonemes=True)
        lang_handler.process = MethodType(lambda self, x: zh.ZHG2P()(x)[0], lang_handler)
    else:
        raise Exception(f"Invalid target language: {lang}")
    return lang_handler