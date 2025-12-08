#Corection des fautes d'orthographe de l'utilisateur
from spellchecker import SpellChecker

spell = SpellChecker()

def correct_spelling(text: str) -> str:
    if not text:
        return ""
    words = text.split()
    corrected = [spell.correction(w) if w else w for w in words]
    return " ".join(corrected)
