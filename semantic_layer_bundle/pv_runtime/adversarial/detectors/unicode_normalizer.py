import unicodedata

class UnicodeNormalizer:

    @staticmethod
    def normalize(text):

        if not isinstance(text, str):
            return text

        return unicodedata.normalize(
            "NFKC",
            text
        )
