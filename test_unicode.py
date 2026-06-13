from pv_runtime.adversarial.detectors.unicode_normalizer import (
    UnicodeNormalizer
)

text = "рrосеss"  # mixed unicode

print(text)

print(
    UnicodeNormalizer.normalize(text)
)
