# -*- coding: utf-8 -*-
# 引入文字识别OCR SDK
from aip import AipOcr

# 百度账号密码 ai.baidu.com去申请,每天免费500次
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''


# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 初始化ApiOcr对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 调用通用文字识别接口
result = aipOcr.basicGeneral(get_file_content('test.jpg'))

# 如果图片是url 调用示例如下
#result = apiOcr.basicGeneral('http://www.xxxxxx.com/img.jpg')


# 百度返回的是个dict
print result

# 读出百度返回的dict
words_num = result['words_result_num']
words = result['words_result']
with open('result.txt', 'w') as f:
    str_num = u'-----找到%s个单词-------\n' % words_num
    print str_num
    f.write(str_num.encode('utf-8'))
    for word in words:
        str_word = word['words'] + u'\n'
        print str_word
        f.write(str_word.encode('utf-8'))