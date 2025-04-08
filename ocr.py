import platform
import pytesseract
from pathlib import Path

class OCRProcessor:
    def __init__(self, tesseract_path=None,lang=None):
        self.lang = lang
        self.tesseract_path = tesseract_path
        self.configure_tesseract(tesseract_path)

    def configure_tesseract(self, path):
        """配置Tesseract路径"""
        if path:
            if Path(path).exists():
                pytesseract.pytesseract.tesseract_cmd = path
                return
        # 如果没有提供路径，则根据操作系统设置默认路径
        if platform.system() == "Windows":
            default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if Path(default_path).exists():
                pytesseract.pytesseract.tesseract_cmd = default_path
            else:
                raise RuntimeError("Tesseract路径未找到，请检查配置")
        elif platform.system() == "Linux":
            default_path = '/usr/bin/tesseract'
            if Path(default_path).exists():
                pytesseract.pytesseract.tesseract_cmd = default_path
            else:
                raise RuntimeError("Tesseract路径未找到，请检查配置")
        elif platform.system() == "Darwin":
            default_path = '/usr/local/bin/tesseract'
            if Path(default_path).exists():
                pytesseract.pytesseract.tesseract_cmd = default_path
            else:
                raise RuntimeError("Tesseract路径未找到，请检查配置")

    def extract_text(self, image):
        """执行OCR识别"""
        try:
            return pytesseract.image_to_string(image,
                                               lang=self.lang,
                                               config='--psm 6').strip()
        except pytesseract.TesseractError as e:
            raise RuntimeError(f"OCR处理失败: {str(e)}")
