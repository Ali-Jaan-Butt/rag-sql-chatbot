from transformers import pipeline


def get_translation_pipeline(src_lang, tgt_lang):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    try:
        return pipeline("translation", model=model_name)
    except:
        return None