#読み込みが悪い文字
#border = 205,{む,ぶ,べ,ぱ,ぴ,ぽ｝
#border = 130,{ふ,ぶ,ぱ,ぴ}

import os
import csv
from PIL import Image
import pyocr
import pyautogui
import pyperclip
import time
import re
import sys

#ここから設定--------------------------------------------------------------

# 探したい文字
searching_word = 'ぬ'
#自分のHPが↓の数字以下だと回復優先
danger_HP_border = 20
#特性がいかすい…True/それ以外…False
ability_is_gastro = True

#ここまで設定--------------------------------------------------------------

#単語周り
used_words = set()
word = ""

with open('dic/dictionary.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

with open('dic/safety_medical.csv','r',encoding = 'utf-8') as medicalFile:
        mD = csv.reader(medicalFile)
        mRows = list(mD)

with open('dic/safety_food.csv','r',encoding = 'utf-8') as foodFile:
        fD = csv.reader(foodFile)
        fRows = list(fD)

#回復制限
medical_limit = 5
food_limit = 6


# メソッド
def search_words_starting_ending_with(start_letter, end_letter):
        
        global medical_limit
        global food_limit

        if(int(myHP) >= danger_HP_border + 1):#HP安全だったら文字探し
            for row in rows:
                word = row[0]
                #探したい文字終わりがあったら出力
                if (word.startswith(start_letter) and word.endswith(end_letter)) or (word.startswith(start_letter) and word.endswith(end_letter + "ー")):
                    if word not in used_words:
                        pyperclip.copy(word)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        used_words.add(word)
                        print("使用単語　：" + word)
                        return
                    
        else:#HPやばかったら回復
            if(medical_limit > 0):
                for row in mRows:
                    word = row[0]

                    if word.startswith(start_letter):
                        if word not in used_words:
                            pyperclip.copy(word)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(0.5)
                            pyautogui.press('enter')
                            used_words.add(word)
                            print("使用単語　：" + word)
                            medical_limit -= 1
                            return
        
            if(food_limit > 0):
                for row in fRows:
                    word = row[0]

                    if word.startswith(start_letter):
                        if word not in used_words:
                            pyperclip.copy(word)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(0.5)
                            pyautogui.press('enter')
                            used_words.add(word)
                            print("使用単語　：" + word)
                            if(not ability_is_gastro):food_limit -= 1
                            return
        #探したい文字終わりがなかったらランダムで出力
        for row in rows:
            word = row[0]

            if word.startswith(start_letter):
                if word not in used_words:
                    pyperclip.copy(word)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    used_words.add(word)
                    print("使用単語　：" + word)
                    return    

def add_margin(pil_img, top, right, bottom, left, color):
        width, height = pil_img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(pil_img.mode, (new_width, new_height), color)
        result.paste(pil_img, (left, top))
        return result
                
            
# 1. インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# 2. OCRエンジンの取得
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print('pyocrが見付かりません。pyocrをインストールして下さい。')
    sys.exit(1)
tool = tools[0]

#↓に入力する数値はマウス座標の(x,y)
pyautogui.click(400,410)#要修正(文字入力欄の右側)
print("約3秒後にスタート")
try:
    i = 0
    while(True):
        pyautogui.sleep(3)

        #ここから文字の認識

        # スクショ撮影
        c = 'word' + str(i) + '.jpg'
        #↓に入力する数値は(四角形の左上のx座標,左上の点のy座標,四角形の横の長さ,四角形の高さ)
        word_photo = pyautogui.screenshot(region=(27, 391, 349, 40))#要修正(「「??」からはじまることば」がすべて写るように)
        word_photo.save(c)

        word_photo_org = Image.open(c)

        print("スクショ撮りました")

        word_photo_org = word_photo_org.convert('RGB')
        size = word_photo_org.size
        word_photo_BandW = Image.new('RGB', size)

        # 白黒化(精度上昇)
        border = 140

        for x in range(size[0]):
            for y in range(size[1]):
                r, g, b = word_photo_org.getpixel((x, y))
                if r < border or g < border or b < border:
                    r = 0
                    g = 0
                    b = 0
                else:
                    r = 255
                    g = 255
                    b = 255
                word_photo_BandW.putpixel((x, y), (r, g, b))

        d = 'word_BW' + str(i) + '.jpg'
        word_photo_BandW.save(d)

        print("白黒にしました")

        #写真サイズ変更
        new_resize='new_resize'+str(i)+'.jpg'

        e = 'word_resize' + str(i) + '.jpg'
        word_photo_new = add_margin(word_photo_BandW, 35, 35, 50, 50, (255, 255, 255))
        word_photo_new.save(e, quality=95)

        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        text = tool.image_to_string(word_photo_new, lang="jpn", builder=builder)
        text = text.replace('「','')
        text = text.replace('」からはじまることば','')
        text = text.replace('」 からはじまることば','')

        if(text == 'ペ'):text = 'ぺ' #ぺがカタカナで認識される
        print("最初の文字：" + text)

        #ここまで文字の認識
        #ここからHPの認識

        f = 'myHP' + str(i) + '.jpg'
        HPphoto = pyautogui.screenshot(region=(327, 333, 70, 22))#要修正(自分HPの??/??がすべて写るように)
        HPphoto.save(f)

        hpBuilder = pyocr.builders.TextBuilder(tesseract_layout=6)
        myHP = tool.image_to_string(HPphoto,lang = "eng",builder = hpBuilder)
        myHP = myHP.replace('/40','')
        myHP = myHP.replace('/50','')
        myHP = myHP.replace('/60','')
        myHP = myHP.replace('/100','')
        myHP = re.sub(r'[^0-9]+', '',myHP)
        print("自分のHP　：" + myHP)

        if len(text) == 1 and len(myHP) != 0:
           search_words_starting_ending_with(text, searching_word)
        
        print("一連の流れ終了")
        os.remove(c)
        os.remove(d)
        os.remove(e)
        os.remove(f)

        print()
        i += 1
except KeyboardInterrupt:
     print("-----------------終了-----------------")
