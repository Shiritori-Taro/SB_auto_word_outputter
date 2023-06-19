# ocr_card.py
import os
from PIL import Image
import pyocr
import pyocr.builders
import pyautogui

# 1.インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# 2.OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 3.原稿画像の読み込み
c = 'test.jpg'
photo = pyautogui.screenshot(region=(27, 391, 349, 40))#要修正(「「??」からはじまることば」がすべて写るように)
photo.save(c)

d='complete_picture.jpg'

photo=photo.convert('RGB')
size=photo.size
img2=Image.new('RGB',size)

#白黒化
border=205
    
for x in range(size[0]):
    for y in range(size[1]):
        r,g,b=photo.getpixel((x,y))
        if r < border or g < border or b < border:
            r = 0
            g = 0
            b = 0
        else:
            r = 255
            g = 255
            b = 255
        img2.putpixel((x,y),(r,g,b))

img2.save(d)
print("スクリーンショットが作成されました。")

# 4.ＯＣＲ実行
builder = pyocr.builders.TextBuilder(tesseract_layout=6)
result = tool.image_to_string(img2, lang="jpn", builder=builder)

print("読み込んだ文字：" + result)