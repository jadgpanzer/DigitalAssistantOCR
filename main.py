import cv2
import yaml
import time
import csv
from pathlib import Path
from logger import Logger
from capture import ScreenCapturer
from ocr import OCRProcessor
from sender import MessageSender


class DigitalAssistantOCR:
    def __init__(self, config_path='config.yaml'):
        self.config = self.load_config(config_path)
        self.logger = Logger(**self.config['logging']).log
        self.capturer = ScreenCapturer(self.config['ocr'].get('region'))
        self.ocr = OCRProcessor(self.config['ocr'].get('tesseract_path'),self.config['ocr'].get('lang'))
        self.sender = MessageSender(self.config['api_endpoints'])
        self.keywords = self.load_keywords()
        self.running = True
        self.last_keywords = None
        self.logger('info', "数字人助手初始化完成")
        self.logger('info', f"当前配置: {self.config}")

    def load_config(self, path):
        """加载YAML配置文件"""
        with open(path) as f:
            config = yaml.safe_load(f)
            
        # 转换区域格式
        if isinstance(config['ocr'].get('region'), list):
            config['ocr']['region'] = tuple(config['ocr']['region'])
            
        return config

    def image_process(self,img):
        """对捕获的图像进行一些简单的处理，包括灰度化和滤波"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
        denoised = cv2.medianBlur(thresh, 3)
        return denoised


    def load_keywords(self):
        """加载关键词映射表"""
        keyword_file = self.config['ocr']['keyword_file']
        try:
            with open(keyword_file, encoding='utf-8-sig') as f:
                return {
                    row['keyword'].strip(): row['response'].strip() or None
                    for row in csv.DictReader(f)
                }
        except Exception as e:
            self.logger('error', f"关键词加载失败: {str(e)}")
            return {}

    def process_text(self, text):
        """处理识别文本"""
        if not text:
            return

        self.logger('info', f"识别到文本: {text[:50]}...")
        
        for keyword, response in self.keywords.items():
            if keyword.casefold() in text.casefold():
                if keyword == self.last_keywords:
                    self.logger('info', f"重复触发关键词: {keyword}")
                    continue
                self.last_keywords = keyword
                self.logger('info', f"触发关键词: {keyword}")
                self.handle_response(keyword, response, text)
                # 考虑到数字人的运行速度，这里选择每次捕获之后只处理一个关键词
                # 如果需要处理多个关键词，可以将下面的break注释掉
                break
        else:
            self.logger('info', "没有匹配的关键词")

    def handle_response(self, keyword, response, original):
        """处理响应逻辑"""
        message = response if response else original
        use_gpt = response is None
        
        try:
            if self.sender.send(message, use_gpt):
                self.logger('info', f"成功发送: {message}")
        except Exception as e:
            self.logger('error', str(e))

    def run(self):
        """主运行循环"""
        self.logger('info', "服务启动")
        try:
            while self.running:
                start_time = time.time()
                try:
                    # 截屏处理流程
                    image = self.capturer.capture()
                    text = self.ocr.extract_text(image)
                    self.process_text(text)
                except Exception as e:
                    self.logger('error', str(e))
                
                # 控制扫描间隔
                elapsed = time.time() - start_time
                sleep_time = max(0, self.config['ocr']['interval'] - elapsed)
                if sleep_time < 0:
                    self.logger('warning', f"处理时间过长: {elapsed:.2f}秒")
                    continue
                # 休眠
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            self.logger('info', "用户中断服务")
        except Exception as e:
            self.logger('critical', f"致命错误: {str(e)}")
        finally:
            self.logger('info', "服务停止")

if __name__ == "__main__":

    
    assistant = DigitalAssistantOCR()
    assistant.run()
