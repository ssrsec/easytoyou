import requests
import os
import re
from shutil import copyfile
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def GetFile(path):
    print('获取文件索引中...')
    file_list=[]
    file_dict={}
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.path.join(root, dir)
            try:
                os.makedirs(('output/'+os.path.join(root, dir)).replace(os.getcwd(),''))
            except:
                print('目录：{}已存在'.format(('output/'+os.path.join(root, dir)).replace(os.getcwd(),'')))

        for f in files:
            file = os.path.join(root, f)

            with open(file,'rb') as f:
                file_body=f.read()
            if file.endswith('.php') == True and b'<?php //004fb' in file_body:
                file_dict[file] = f
                file_list.append(file)
            else:
                copyfile(file, ('output/' + file).replace(os.getcwd(),''))
    return file_list


def UploadFile(file):
    print('进度：{}/{}'.format(str(a),str(b)))
    headers={
        'Cache-Control': 'max-age=0',
        'Origin': 'https://easytoyou.eu',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryAc5jjAUPcH1aruyG',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.109 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': 'https://easytoyou.eu/decoder/ic10php71',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '替换成你自己的cookie'

    }
    proxy = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

    try:
        filename_res = requests.get('https://easytoyou.eu/decoder/ic10php71', headers=headers,timeout=25,verify=False,proxies=proxy)
        filename = re.findall(r"file\" name=\"(.+?)\"", filename_res.text)[0]
        with open(file,'r') as f:
            php=f.read()
        data='''------WebKitFormBoundaryAc5jjAUPcH1aruyG
Content-Disposition: form-data; name="{}"; filename="broadcasting.php"
Content-Type: text/php

{}
------WebKitFormBoundaryAc5jjAUPcH1aruyG
Content-Disposition: form-data; name="submit"

Decode
------WebKitFormBoundaryAc5jjAUPcH1aruyG
'''.format(filename,php)
        res = requests.post('https://easytoyou.eu/decoder/ic10php71',headers=headers,data=data,timeout=25,verify=False,proxies=proxy)
        if res.status_code == 200 and re.findall(r"Download link: <a href='", res.text) != []:
            print(file + '上传成功')
            download = re.findall(r"Download link: <a href='(.+?)'>",res.text)[0]
            down_res = requests.get(download,headers=headers, timeout=25)
            if res.status_code==403:
                print('下载出错')
                with open('error.txt', 'a') as f:
                    f.write(file + '下载出错\n')
            else:
                with open(('output/' + file).replace(os.getcwd(),''), "wb") as code:
                    code.write(down_res.content)
                print(file + '下载成功')
        elif re.findall(r"can't be decoded.", res.text) != []:
            copyfile(file, ('output/' + file).replace(os.getcwd(),''))
            print('未加密或类型不正确：'+file)
        else:
            print('其他请求错误')
            with open('error.txt', 'a') as f:
                f.write(file + '其他请求错误\n')
    except:
        print('上传请求出错')
        with open('error.txt','a') as f:
            f.write(file+'上传请求出错\n')



AllFile=GetFile('www/')
a=0
b=len(AllFile)
for file in AllFile:
    a+=1
    UploadFile(file)
