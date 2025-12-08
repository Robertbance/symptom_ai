# traduction du texte utilisateur
from deep_translator import GoogleTranslator

def translate_fr_en(text: str) -> str:
    """Traduction FR → EN"""
    if not text or not isinstance(text, str):
        return ""

    try:
        t = GoogleTranslator(source="fr", target="en").translate(text)
        return t if t else text
    except:
        return text


def translate_en_fr(text: str) -> str:
    """Traduction EN → FR"""
    if not text or not isinstance(text, str):
        return ""

    try:
        t = GoogleTranslator(source="en", target="fr").translate(text)
        return t if t else text
    except:
        return text
