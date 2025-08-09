import urllib.request
import urllib.parse
# 导入requests库
import requests


def run1():
     url = 'https://www.itcast.cn'
     header = {
          "User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT6.1;Trident/5.0)",
          "Host" : "httpbin.org"
     }
     dict_demo = {"name": "itcast"}
     data = bytes(urllib.parse.urlencode(dict_demo).encode('utf-8'))
     # 将url作为Request方法的参数，构造并返回一个Request对象
     request = urllib.request.Request(url, data=data, headers=header)
     # 将Request对象作为urlopen方法的参数，发送给服务器并接收响应
     response = urllib.request.urlopen(request)
     # 使用read方法读取获取到的网页内容
     html = response.read().decode('UTF-8')
     # 打印网页内容
     print(html)

def run2():
     # 调用urllib.request库的urlopen方法，并传入一个url
     response = urllib.request.urlopen('http://127.0.0.1:80/')
     # 使用read方法读取获取到的网页内容
     html = response.read().decode('UTF-8')
     # 打印网页内容
     print(html)

def run3():

     # 请求的URL路径和查询参数
     url = "http://www.baidu.com/s"
     word = {"wd": "传智播客"}
     # 转换成url编码格式（字符串）
     word = urllib.parse.urlencode(word)
     # 拼接完整的URL路径
     new_url = url + "?" + word
     # 请求报头
     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 51.0.2704.103 Safari / 537.36"}
     # 根据URL和headers构建请求
     request = urllib.request.Request(new_url, headers=headers)
     # 发送请求，并接收服务器返回的文件对象
     response = urllib.request.urlopen(request)
     # 使用read方法读取获取到的网页内容，使用UTF-8格式进行解码
     html = response.read().decode('UTF-8')
     print(html)

def run4():
     # 请求的URL路径和查询参数
     url = "http://www.baidu.com/s"
     param = {"wd": "传智播客"}
     # 请求报头
     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 51.0.2704.103 Safari / 537.36"}
     # 发送GET请求，返回一个响应对象
     response = requests.get(url, params=param, headers=headers)
     # 查看响应的内容
     print(response.text)
#      函数	                            功能说明
# requests.request()	 构造一个请求，支撑以下各方法的基础方法
# requests.get()	     获取HTML网页的主要方法，对应于HTTP的GET请求方式
# requests.head()	     获取HTML网页头信息的方法，对应于HTTP的HEAD请求方式
# requests.post()	     向HTML网页提交POST请求的方法，对应于HTTP的POST请求方式
# requests.put()	     向HTML网页提交PUT请求的方法，对应于HTTP的PUT请求方式
# requests.patch()	     向HTML网页提交局部修改请求，对应于HTTP的PATCH请求方式
# requests.delete()	     向HTML网页提交删除请求，对应于HTTP的DELETE请求方式

def run5():
     file = open('index.html', 'w', encoding='utf-8')
     file.write("hello word!!!")
     file.close()

if __name__ == "__main__":
    # 批量提交问卷
    run5()