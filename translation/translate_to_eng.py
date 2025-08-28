from translation import get_translation
import langdetect


def translate_to_english(text):
    try:
        lang = langdetect.detect(text)
        if lang == "en":
            return text, "en"
        translator = get_translation.get_translation_pipeline(lang, "en")
        if translator:
            translated = translator(text, max_length=512)[0]['translation_text']
            return translated, lang
    except:
        pass
    return text, "en"