import subprocess
import sys
from PIL import ImageGrab
import platform
import numpy as np
class ScreenCapturer:
    def __init__(self, region=None):
        self.region = self.validate_region(region)

    def validate_region(self, region):
        """验证区域格式"""
        try:
            screen_width, screen_height = ImageGrab.grab().size
            if region == 'full':
                return (0,0,screen_width,screen_height)
            if region == 'manually':
                return self.select_region_manually()
            else:
                x,y,x1,y1 = region
                return (x,y,x1,y1)
        except Exception as e:
            print(f"屏幕捕获区域配置故障:{str(e)}")
            sys.exit(1)

    def select_region_manually(self):
        """使用slop选择区域"""
        print("[System] 请在屏幕上选择区域...")
        try:
            output = subprocess.check_output(
                ["slop", "--format=%x,%y,%w,%h"]
            ).decode().strip()
            x, y, w, h = map(int, output.split(','))
            return (x, y, x+w, y+h)
        except Exception as e:
            print(f"[Error] 手动区域选择失败：{str(e)}")
            sys.exit(1)

    def capture(self):
        """执行屏幕捕获"""  
        try:
            img = ImageGrab.grab(bbox=(self.region))
            return np.array(img,dtype=None,copy=None)
        except Exception as e:
            raise RuntimeError(f"屏幕捕获失败: {str(e)}")
