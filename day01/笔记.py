# from urllib import request
# url = "http://www.baidu.com"
# response = request.urlopen(url)
# print(response)

# from urllib import request, parse
#
# url = "https://www.iqianyue.com/mypost"
# dict1 = {"name":"python","pass":"123455"}
# data = bytes(parse.urlencoding(dict1),encoding='utf-8')
# result = request.urlopen(url,data=data).read()
# print(result)

# from urllib import request
# import json
# url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%8C%AB%E5%92%AA&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%E7%8C%AB%E5%92%AA&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=30&rn=30&gsm=1e&1595572249656="
# res = request.urlopen(url).read()
# data = json.loads(res.decode('utf-8'))
# for img in data['data']:
#     if img:
#         print(img['middleURL'])
# import re
# res = request.urlopen(url).read().decode('utf-8')
# rule = '"midleURL":"(.*?)",'
# result = re.findall(rule,res)
# print(result)

from urllib import request
import gzip
from lxml import etree
main_url  =  "http://www.xbiquge.la/xiaoshuodaquan/"
res = request.urlopen(main_url).read()
new_res = gzip.decompress(res).decode("utf-8")
ele  = etree.HTML(new_res)
book_urls = ele.xpath('//div[@id="main"]/div/ul/li/a/@href')
book_names = ele.xpath('//div[@id="main"]/div/ul/li/a/text()')
for book_url in book_urls:
    index = book_urls.index(book_url)
    book_name = book_names[index]
    book_res = request.urlopen(book_url).read()
    try:
        new_book_res = gzip.decompress(book_res).decode('utf-8')
    except:
        new_book_res = book_res
    ele = etree.HTML(new_book_res)
    cha_urls = ele.xpath('//div[@id="list"]/dl/dd/a/@href')
    new_cha_urls = ['http://www.xbiquge.la'+ url for url in cha_urls]
    print(cha_urls)
    for cha_url in new_cha_urls:
        detail_res = request.urlopen(cha_url).read()
        new_detail_res = gzip.decompress(detail_res).decode('utf-8')
        ele = etree.HTML(new_detail_res)
        content = ele.xpath('//div[@id="content"]/text()')
        cha_name =ele.xpath('//h1/text()')[0]
        s = ""
        print(cha_name,content)
        for cont in content:
            s+=cont
        with open(book_name+".txt",'a',encoding='utf-8') as w:
            w.write(cha_name +"\n"+s+"\n")