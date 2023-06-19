import pyautogui
try:
    while True:
        x,y = pyautogui.position()
        position = 'X:'+str(x)+'  '+ 'Y: '+str(y)
        print(position)
        pyautogui.sleep(1)
except KeyboardInterrupt:
    print('\n終了')