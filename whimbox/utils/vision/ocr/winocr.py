import numpy as np
from typing import Tuple, List
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.globalization import Language
from whimbox.utils.vision.ocr.base import OCREngine
from whimbox.utils.windows_utils import numpy_array_to_software_bitmap, wait_for

class WinOCREngine(OCREngine):
    def __init__(self, config: dict):
        self.lang = config.get("lang", "zh-Hans")

    def recognize(self, image: np.ndarray) -> List[Tuple[str, Tuple]]:
        software_bitmap = numpy_array_to_software_bitmap(image=image)

        ocr_engine = OcrEngine.try_create_from_language(Language(self.lang))

        if not ocr_engine:
            raise RuntimeError("Failed to create OCR engine")

        result = wait_for(ocr_engine.recognize_async(software_bitmap))

        return result.text, None