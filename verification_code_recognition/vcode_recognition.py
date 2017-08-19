# -*- coding: utf-8 -*-
import traceback


# -----识别数字型图片验证码-----
# input: file path
# output:  numerical verification code (str)
# note: numerical vcode only！
def extract_number_from_image(image_path):
    # 先检查是否有环境
    try:
        from PIL import Image, ImageEnhance, ImageFilter
        from pytesser import image_to_string
    except:
        print traceback.format_exc()
        return
    # 可能吧数字误识别成字母，最后做个替换
    rep = {
           'O': '0',
           'I': '1',
           'L': '1',
           'Z': '2',
           'S': '8',
           'B': '8'
           }
    # 二值化
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 开始识别
    with Image.open(image_path) as im:
        itype = image_path.split('.')[-1]
        ipath = image_path.split('.')[0]
        # 转化到灰度图
        imgry = im.convert('L')
        imgry.save(ipath + '_g.' + itype)  # 保存灰度图
        out = imgry.point(table, '1')  # 二值化，采用阈值分割法，threshold为分割点
        out.save(ipath + '_b.' + itype)
        text = image_to_string(out)  # 识别
        # 处理误识别
        text = text.strip()
        text = text.upper()
        for r in rep:
            text = text.replace(r, rep[r])
        return text


if __name__ == '__main__':
    vcode = extract_number_from_image("vcode.jpg")
    print vcode