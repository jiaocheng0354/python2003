import gzip
from urllib import request
from lxml import etree

from day01.databases import Database

# 记录总数
# def creat_data(statr_page,end_page):
def creat_data(statr_page,end_page):
    num = 0
    for i in range(statr_page,end_page):
        job_url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE,2,'+str(i)+'.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        print("")
        # 判断当前页是否爬取
        database = Database("count_url")
        if database.get_page(i):
            print("endpage%-8s" % i)
            continue
        response = request.urlopen(job_url).read().decode('gbk')
        ele = etree.HTML(response)
        job_urls = ele.xpath('//div[@class="el"]/p/span/a/@href')
        job_text = ele.xpath('//div[@class="el"]/p/span/a/text()')
        job_company = ele.xpath('//div[@class="el"]/span[@class="t2"]/a/text()')
        job_city = ele.xpath('//div[@class="el"]/span[@class="t3"]/text()')
        job_add_data = ele.xpath('//div[@class="el"]/span[@class="t5"]/text()')
        count = 0
        page = i
        print("%-8s" % i)
        for index, url in enumerate(job_urls):
            data = []
            count += 1
            # print(url)
            # 查询 是否爬取
            database = Database("work")
            if database.get(url):
                continue
            try:
                response = request.urlopen(url,timeout=3).read().decode('gbk')
                ele = etree.HTML(response)
            except:
                count -= 1
                # 记录爬取异常链接
                database = Database("error")
                keys = ["page", "url"]
                values = [page, url]
                database.set(keys, values)
                continue
            else:
                job_salary = ele.xpath('//div[@class="cn"]/strong/text()')
                job_detail = ele.xpath('//div[@class="cn"]/p/@title')
                data.append(job_urls[index])
                data.append(str(job_text[index]).replace(r'\r\n', ''))
                data.append(job_company[index])
                data.append(job_city[index])
                data.append(job_add_data[index])
                data.append(str(job_salary))
                data.append(str(job_detail).replace(r'\xa0\xa0|\xa0\xa0', '|'))
                # print(data)
                # 保存数据
                database = Database("work")
                keys = ["url", "text", "company", "city", "add_data", "salary", "detail"]
                # values = ["Mr_lee","html","202"]
                database.set(keys, data)
                print("%3s" % index, end='')

        # 统计结果 保存
        database = Database("count_url")
        keys = ["count", "page", "url"]
        values = [count - 1, page, url]
        database.set(keys, values)
        num = num + count - 1
        # print("page%-8s"%page)
    print("页数", i, "总数", num)
if __name__ == '__main__':
    creat_data(1,1089)
