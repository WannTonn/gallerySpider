'''
Author: WannTonn
Date: 2021-03-21 15:28:30
LastEditTime: 2021-05-06 20:53:14
LastEditors: WannTonn
Description: 
FilePath: /gallerySpider/bsoup.py
'''

from bs4 import BeautifulSoup
import requests


def spiders():
    # 控制爬取的页数，并开始爬取
    for i in range(15):
        if i < 15:
            spider(i)


def spider(page):
    imgs_arr = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (HTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36'}
    url = '{url}/{page}/'.format(url='',page=page + 1)  # !!注意。这里的URL填写需要爬取的网站
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.content, 'lxml')

    for link in soup.findAll(class_='masonry-item'):
        link_item = link.find('a')['href']
        name = link['id']
        imgs_arr.append({'href': link_item, 'name': name})
    for i in range(len(imgs_arr)):
        img = imgs_arr[i]
        # 以下为根据页面dom元素结构写的配置
        img_res = requests.get(img['href'], headers=headers)
        img_res.encoding = 'utf-8'
        img_soup = BeautifulSoup(img_res.content, 'lxml')
        wrapper = img_soup.find('section', id='post')
        items = wrapper.find_all('figure')
        for k in range(len(items)):
            item = items[k]
            src = item.find('img')['src']
            file_name = '{name}_{index}'.format(name=img['name'], index=k + 1)
            print("--- 正在爬取 第{page}页的 {name} / {length} ---".format(name=file_name, page=page, length=len(items)))
            img = requests.get(src, headers=headers, timeout=60)
            with open('pics/{name}.jpg'.format(name=file_name), 'wb') as f:
                f.write(img.content)
                f.close()


if __name__ == '__main__':
    spiders()
