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
            if file.endswith('.php') == True:
                file_dict[file] = f
                file_list.append(file)
            else:
                copyfile(file, ('output/' + file).replace(os.getcwd(),''))
    return file_list


def UploadFile(file):
    print('进度：{}/{}'.format(str(a),str(b)))
    headers={
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-User': '?1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '替换成你的cokie'

    }
    proxy = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

    try:
        filename_res = requests.get('https://easytoyou.eu/decoder/ic10php56', headers=headers,timeout=25,verify=False)
        filename = re.findall(r"file\" name=\"(.+?)\"", filename_res.text)[0]
        res = requests.post('https://easytoyou.eu/decoder/ic10php56',headers=headers ,files={filename: open(file, 'rb')},data={'submit':'Decode'},timeout=25,verify=False)
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



AllFile=GetFile('tq/')
a=0
b=len(AllFile)
for file in AllFile:
    a+=1
    UploadFile(file)
