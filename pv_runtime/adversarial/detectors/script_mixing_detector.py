class ScriptMixingDetector:

    def score(self, text=""):

        if not text:
            return 0

        latin = False
        cyrillic = False

        for ch in text:

            code = ord(ch)

            if (
                0x0041 <= code <= 0x007A
            ):
                latin = True

            if (
                0x0400 <= code <= 0x04FF
            ):
                cyrillic = True

        if latin and cyrillic:
            return 30

        return 0
