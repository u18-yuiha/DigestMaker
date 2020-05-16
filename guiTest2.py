import pyautogui

auth_flag = pyautogui.prompt('パスワードを入力してください','ログイン認証')
print('password>>',auth_flag)