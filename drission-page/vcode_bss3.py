import io

from PIL import Image


def image_code():
    text = '''{"code":"0000","message":"èŽ·å–éªŒè¯ç æˆåŠŸ","respDate":"2024-02-28 14:38:13","status":200,"path":"/login/graphic-code"}'''

    txt16 = 'èŽ·å–éªŒè¯ç æˆåŠŸ'
    # with open('img2.txt', 'r') as file:
    #     hex_string = file.read().strip()

    try:
        txt_bytes = bytes.fromhex(txt16)
        txt = txt_bytes.decode('utf-8')
        print(txt)
    except UnicodeDecodeError:
        print("Not UTF-8 encoded")

if __name__ == '__main__':
    image_code()