from translation import get_translation


def translate_from_english(text, target_lang):
    if target_lang == "en":
        return text
    translator = get_translation.get_translation_pipeline("en", target_lang)
    if translator:
        translated = translator(text, max_length=512)[0]['translation_text']
        return translated
    return text