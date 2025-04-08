# DigitalAssistantOCR

在AI无人直播中，用于Fay数字人框架的评论OCR识别+关键词回复

## 前期准备

在运行这个项目之前，你需要先配置好Fay数字人框架，具体可以参考这篇文档：
https://qqk9ntwbcit.feishu.cn/wiki/JzMJw7AghiO8eHktMwlcxznenIg

在Fay安装完成后，还需要确保文字交互接口（5000）是开放的，因为本项目使用到了该接口，使用以下命令确保该接口没有被占用：

```
netstat -tunlp |grep 5000
```
## 安装

安装相关依赖：

```
pip install requirements.txt
```

手动配置tessertact位置，在config.yaml里面修改如下词条为你的安装路径：
```
ocr:
	.......
    tesseract_path: # linux：/usr/bin/tesseract or windows：C:\Program Files\Tesseract-OCR\tesseract.exe 
	.......
```
## 开始使用

运行主函数即可：
```
python main.py
```

## 参数解读
```config.yaml```为配置文件，下面是对该文件中一些参数的解释：

```region```: 捕获区域，'manually'为手动指定捕获区域；'full'为全屏幕；还可以使用四元数组来制定，其格式为[左上角坐标x，左上角坐标y，右下角坐标x，右下角坐标y]

```interval```: 捕获间隔（s），默认为10秒，这里可以根据配置来调整

```tesseract_path```: pytesseract的路径，linux下为文件夹路径，windows下为exe可执行文件路径

```keyword_file```: 关键词文档路径，关键词文档以“keyword-response”键值对组成，keyword不能重复。当response不为空时，将提前预设好的回复台词发送给Fay，Fay根据预设的回复合成语音；反之，Fay使用LLM合成回复（建议设置好回复词）

```lang```: OCR识别文字类型，默认为“chi_sim+eng”即简体中文和英文

```gpt_endpoint, transparent_endpoint```: 这是Fay框架预设的端口，不建议更改
