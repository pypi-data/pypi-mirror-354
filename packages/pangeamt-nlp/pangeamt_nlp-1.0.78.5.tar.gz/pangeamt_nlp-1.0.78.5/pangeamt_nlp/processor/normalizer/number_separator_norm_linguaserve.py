from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg

from babel.numbers import parse_decimal, format_decimal
from babel.core import Locale
from decimal import Decimal
import re

class NumberIdentificationHelpers:
    # First element: thousands separator. Second: comma symbol
    # Note: rules change from country to country, even within Europe (e.g. Swiss German, Austrian German, German German)
    # Note: I could not find an official source for most languages. However, the usage of space as thousand separator
    #   (either non-seperable space or thin space) is accepted (almost?) everywhere
    # Source for the linguistic information not verified by linguists:
    #   https://en.wikipedia.org/wiki/Decimal_separator#Examples_of_use

    STANDARD_SEPARATORS_PER_LANGUAGE = {
        "cs": ("\u00A0", ","),  # Not verified by linguist, czech
        "da": ("\u00A0", ","),  # Not verified by linguist
        "de": (".", ","),  # Not verified by linguist
        "en": (",", "."),  # Verified online and by myself
        "es": ("\u00A0", ","),  # Verified with Yaiza
        "ca": ("\u00A0", ","),  # Verified with MAG
        "fr": ("\u00A0", ","),  # Verified with Cath
        "it": ("\u00A0", ","),  # Not verified by linguist
        "nl": (".", ","),  # Not verified by linguist
        "hr": (".", ","),  # Not verified by linguist, Croatian
        "mt": (",", "."),  # Maltese, not verified by linguist
        "pt": ("\u00A0", ","),  # Not verified by linguist
    }

    @classmethod
    def convert(cls, text, src_lang: str, tgt_lang: str):
        try:
            # Paso 1: Parsear el número según el idioma de origen
            decimal_number = parse_decimal(text, locale=src_lang)

            # Paso 2: Formatear el número al idioma de destino
            converted_number = format_decimal(decimal_number, locale=tgt_lang)

            return converted_number
        except Exception as e:
            return text

    @classmethod
    def custom_convert(cls, text: str, src_lang: str, tgt_lang: str):

        if re.search(r'\d{4,}[.,]\d+', text) is not None:
            return text
        sep_th_src, sep_decimal_src = NumberIdentificationHelpers.STANDARD_SEPARATORS_PER_LANGUAGE[
            src_lang]
        sep_th_tgt, sep_decimal_tgt = NumberIdentificationHelpers.STANDARD_SEPARATORS_PER_LANGUAGE[
            tgt_lang]

        # Paso 1: Normalizar el número: quitar separadores de miles y reemplazar decimal por '.'
        normalized_number = text.replace(sep_th_src, '').replace(" ", "")
        # normalized_number = normalized_number.replace(sep_decimal_src, ',')
        # normalized_number = NumberIdentificationHelpers.clean_intermediate_dot(normalized_number)
        # normalized_number = parse_decimal(normalized_number, locale=src_lang)
            
        
        try:
            # number = float(normalized_number)
            # number = Decimal(normalized_number)
            number = parse_decimal(normalized_number, locale=src_lang)
        except Exception:
            return text
        
        # Paso 1: Normalizar el número: quitar separadores de miles y reemplazar decimal por '.'
        # normalized_number = text.replace(sep_th_src, '').replace(" ", "")
        # normalized_number = normalized_number.replace(sep_decimal_src, ',')
        # normalized_number = NumberIdentificationHelpers.clean_intermediate_dot(normalized_number)
        # normalized_number = parse_decimal(normalized_number, locale=src_lang)
            
        
        # try:
        #     # number = float(normalized_number)
        #     number = Decimal(normalized_number)
        # except Exception:
        #     return text


        # Paso 2: Formatear con separadores destino
        part_int, _, part_decimal = f"{number:.15f}".partition('.')
        part_int_with_th = NumberIdentificationHelpers.insert_thousands_separators(
            text=part_int, separator=sep_th_tgt)

        if int(part_decimal) == 0:
            return f"{part_int_with_th}"
        else:
            part_decimal_cleaned = part_decimal.rstrip('0')
            return f"{part_int_with_th}{sep_decimal_tgt}{part_decimal_cleaned}"

    @classmethod
    def insert_thousands_separators(cls, text, separator: str):
        parts = []
        while text:
            parts.insert(0, text[-3:])
            text = text[:-3]
        return separator.join(parts)
    
    @classmethod
    def clean_intermediate_dot(cls,text):
        if text.count('.') <= 1:
            return text
        # Mantener solo el último punto como decimal
        partes = text.split('.')
        return ''.join(partes[:-1]) + '.' + partes[-1]

    @classmethod
    def is_number_in_target_format(cls,text: str, sep_th: str, sep_decimal: str) -> bool:
        # Escapar separadores para regex
        if text.count(sep_decimal) > 1:
            return False
        index_decimal = text.rfind(sep_decimal)
        index_th = text.rfind(sep_th)
        return  index_th < index_decimal


    @classmethod
    def get_standard_separators_for_language(cls, language_code):
        if language_code in cls.STANDARD_SEPARATORS_PER_LANGUAGE.keys():
            return cls.STANDARD_SEPARATORS_PER_LANGUAGE[language_code]
        else:
            raise ValueError(
                "No number separators have been defined for language code " + language_code)

    @classmethod
    def has_standard_separators_for_language(cls, language_code):
        return language_code in cls.STANDARD_SEPARATORS_PER_LANGUAGE.keys()


class NumberSeparatorNormLinguaServe(NormalizerBase):
    """Note: cannot be used together with CurrencyNorm, because they both have a different way to break
    ambiguity when identifying numbers."""

    NAME = "number_separator_norm_linguaserve"

    DESCRIPTION_DECODING = """
        Normalizes all numbers in the target to conform to the rules of the language concerning the
        separators for thousands and the decimal character (e.g. 1.000.100,05 or 1,000,100.05). Reverts to a 
        standard rule if no explicit rules for the language are defined
        WARNING: DO NOT USE TOGETHER WITH CurrencyNorm
    """

    def __init__(self, src_lang, tgt_lang):
        super().__init__(src_lang, tgt_lang)

    # Called when training
    def process_train(self, seg: Seg) -> None:
        pass

    # Called when using model (before calling model to translate)
    def process_src_decoding(self, seg: Seg) -> None:
        pass

    # Called after the model translated (in case this would be necessary; usually not the case)
    def process_tgt_decoding(self, seg: Seg) -> None:
        if NumberIdentificationHelpers.has_standard_separators_for_language(self.get_tgt_lang()):
            gold_tgt = NumberIdentificationHelpers.custom_convert(
                    text=seg.tgt, src_lang=self.get_tgt_lang(), tgt_lang=self.get_tgt_lang())
            if seg.tgt != gold_tgt:
                if NumberIdentificationHelpers.has_standard_separators_for_language(self.get_src_lang()):
                    seg.tgt = NumberIdentificationHelpers.custom_convert(
                        text=seg.tgt, src_lang=self.get_src_lang(), tgt_lang=self.get_tgt_lang())
                else:
                    seg.tgt = NumberIdentificationHelpers.convert(text=seg.tgt,
                                                                src_lang=self.get_src_lang(),
                                                                tgt_lang=self.get_tgt_lang()
                                                                )
