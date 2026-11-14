"""MeaningGuard translation helpers backed by Meta's NLLB-200 model."""

from functools import lru_cache
from typing import Dict

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


MODEL_NAME = "facebook/nllb-200-distilled-600M"
LANGUAGE_CODES: Dict[str, str] = {
    "en": "eng_Latn",
    "english": "eng_Latn",
    "fr": "fra_Latn",
    "french": "fra_Latn",
    "sw": "swh_Latn",
    "swahili": "swh_Latn",
}


class NLLBTranslator:
    """Reusable translator for English, French, and Swahili using NLLB-200."""

    # Initialize the tokenizer and model once so repeated translations can reuse them.
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    # Translate text between supported languages, for example en -> fr or sw -> en.
    def translate(self, text: str, source_language: str, target_language: str) -> str:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            return ""

        source_code = self._language_code(source_language)
        target_code = self._language_code(target_language)
        self.tokenizer.src_lang = source_code
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        target_token_id = self.tokenizer.convert_tokens_to_ids(target_code)

        with torch.inference_mode():
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=target_token_id,
                max_new_tokens=512,
            )

        return self.tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True
        )[0]

    # Resolve a user-friendly language name or abbreviation to an NLLB language code.
    @staticmethod
    def _language_code(language: str) -> str:
        normalized = language.strip().lower()
        try:
            return LANGUAGE_CODES[normalized]
        except (AttributeError, KeyError):
            supported = ", ".join(sorted(LANGUAGE_CODES))
            raise ValueError(
                f"Unsupported language {language!r}. Use one of: {supported}."
            ) from None


# Cache a single model instance so the convenience functions do not reload model weights.
@lru_cache(maxsize=1)
def _get_default_translator() -> NLLBTranslator:
    return NLLBTranslator()


# Translate English text into French.
def english_to_french(text: str) -> str:
    return _get_default_translator().translate(text, "en", "fr")


# Translate French text into English.
def french_to_english(text: str) -> str:
    return _get_default_translator().translate(text, "fr", "en")


# Translate English text into Swahili.
def english_to_swahili(text: str) -> str:
    return _get_default_translator().translate(text, "en", "sw")


# Translate Swahili text into English.
def swahili_to_english(text: str) -> str:
    return _get_default_translator().translate(text, "sw", "en")


# Export the reusable translator and supported direction-specific functions.
__all__ = [
    "NLLBTranslator",
    "english_to_french",
    "french_to_english",
    "english_to_swahili",
    "swahili_to_english",
]
