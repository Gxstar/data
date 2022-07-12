import os
import time
import ast
import urllib.parse

import requests
from bs4 import BeautifulSoup

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
}


# 获得网页内容
def get_link(keywords: str, num: int):
    first = 0
    count = 0
    name = urllib.parse.quote(keywords)
    if not os.path.exists(f'./image/{keywords}'):
        os.mkdir(f'./image/{keywords}')
    while count < num:
        url = f'https://cn.bing.com/images/async?q={name}&first={first}&count=35&relp=35&lostate=r&mmasync=1'
        first = first + 35
        content = requests.get(url, headers=header).content.decode('utf-8')
        soup = BeautifulSoup(content, 'lxml')
        length = len(soup.select('.iusc'))
        for item, j in enumerate(soup.select('.iusc')):
            if count >= num:
                return False
            print(f'当前请求第{count + 1}张，共{num}张', end='\r')
            link = ast.literal_eval(j.attrs['m'])['murl']
            order = len(os.listdir(f'./image/{keywords}')) + 1
            save_img(link, keywords, order)
            count = count + 1


# 保存图片
def save_img(url: str, keywords: str, num: int):
    try:
        time.sleep(0.2)
        r = requests.get(url, stream=True, headers=header)
        if r.status_code == 200:
            open(f'./image/{keywords}/img_{keywords}_{num}.png', 'wb').write(r.content)
        del r
    except Exception:
        time.sleep(0.2)
        print('产生未知错误！')


def main():
    keywords = '北京'
    num = 37
    get_link(keywords, num)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
