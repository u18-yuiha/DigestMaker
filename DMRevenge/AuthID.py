import socket
import uuid
import sys
import os
import COMPONENT.BasicErrorComponent as BEC

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def register_ID():
    s = uuid.getnode()
    s = str(s)
    try:
        with open(resource_path('ID.text'), mode='x') as f:
            f.write(s)
    except FileExistsError:
        pass
def authentication():
    with open(resource_path('ID.text')) as f:
        s = f.read()
        s = int(s)
    auth_flag = True   
    ID = uuid.getnode()
    if ID == s:
        return auth_flag
    else:
        auth_flag = False
        BEC.show_info("IDが一致しませんでした。\nこのアプリの初回起動時のパソコンでご使用なさってください。\nもしくは今お使いのパソコンに再度アプリをインストールしてください")
        return auth_flag