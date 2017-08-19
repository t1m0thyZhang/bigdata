爬虫模拟登录很多时候会遇到验证码问题

往往登陆的formdata需要带验证码

如果不能识别自动验证码，就需要每次人工启动爬虫

vcode_recognition.py实现了识别数字型验证码的识别

不过，本脚本基于hashprint的识别方法成功率很低，只能识别很low的数字验证码。

一旦有较多的噪声则会误识别或失败

-------------------------------------
call_baidu_ocr.py

调用百度接口
每天免费500次
http://ai.baidu.com/tech/ocr?castk=LTE%3D # 项目地址
https://ai.baidu.com/docs#/OCR-Python-SDK/top?qq-pf-to=pcqq.c2c  # 文档地址

输入test.jpg
识别结果写入result.txt


