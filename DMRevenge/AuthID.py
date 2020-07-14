import socket
import uuid
import COMPONENT.BasicErrorComponent as BEC
def register_ID():
    s = uuid.getnode()
    s = str(s)
    try:
        with open('ID.text', mode='x') as f:
            f.write(s)
    except FileExistsError:
        pass
def authentication():
    with open('ID.text') as f:
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