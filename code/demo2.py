'''
目标：爬去京东上防脱发前十页的信息(名称，价格，销量，产地)
思路：获取网页源代码－－＞正则表达式筛选－－＞保存到excal表格中
'''
from bs4 import BeautifulSoup
import pandas as pd
import request
import re
import time
# from selenium import webdriver
time1 = time.time()

import requests
count = 0 #计数器
number = []
flags = []
names = []
prices = []
sale = []
provider = []
product = []
exception = []
#########################分析网页规律################################
'''
https://search.jd.com/Search?keyword=%E9%98%B2%E8%84%B1%E5%8F%91&enc=utf-8&wq=%E9%98%B2%E8%84%B1%E5%8F%91&pvid=cab14b71884a47d1bc747d49ebc5c8d6
https://search.jd.com/Search?keyword=%E9%98%B2%E8%84%B1%E5%8F%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%98%B2%E8%84%B1%E5%8F%91&stock=1&page=1&s=1&click=0
https://search.jd.com/Search?keyword=%E9%98%B2%E8%84%B1%E5%8F%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%98%B2%E8%84%B1%E5%8F%91&stock=1&page=3&s=61&click=0
https://search.jd.com/Search?keyword=%E9%98%B2%E8%84%B1%E5%8F%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%98%B2%E8%84%B1%E5%8F%91&stock=1&page=5&s=121&click=0
https://search.jd.com/Search?keyword=%E9%98%B2%E8%84%B1%E5%8F%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%98%B2%E8%84%B1%E5%8F%91&stock=1&page=7&s=181&click=0
'''
#读取网页内容
def getHtmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(url)
        print('success')
        return r.text
    except:
        print('fail')
        return 'false'

#商品产地一直无法抓取到，原因可能是由于js动态加载的缘故
def parseProduct(product_html):
    product_soup = BeautifulSoup(product_html,'html.parser')
    # if product_soup.find('div',class_='Ptable') == None:
    product_provider = 0
    key_element = product_soup.find('div',class_='p-parameter').find_all('li')
    for k in range(len(key_element)):
        if '商品产地' in str(key_element[k].next_element):
            product_provider = key_element[k]['title']
            break
        else:
            product_provider = -1
    if product_provider == -1:
        key_element= product_soup.find('div',class_="Ptable-item")
        if key_element !=None:
            key_element = key_element.find_all('dl',class_='clearfix')
            for i in range(len(key_element)):
                if key_element[i].find('dt').string == '产地':
                    product_provider = key_element[i].find('dd').string
                else:
                    product_provider = -2
        else:
            pass
    return product_provider
    # else:
    #     key_element= product_soup.find('div',class_="Ptable-item").find_all('dl',class_='clearfix')
    #     for i in range(len(key_element)):
    #         if key_element[i].find('dt').string == '产地':
    #             product_provider = key_element[i].find('dd').string
    
 

def parseHtml(html,num):
    soup = BeautifulSoup(html,'lxml') #之前碰到的一个bug一直出在解析器这一块
    list = soup.find_all('li',class_='gl-item')


    for i in range(len(list)):
        try:
            
            #获取商品的名称信息
            product_name = list[i].find('div',class_='p-name p-name-type-2').em.string
            if product_name == None:
                product_name = list[i].find('div',class_='p-name p-name-type-2').em.contents[1]
                if list[i].find('div',class_='p-name p-name-type-2').em.span == None:
                    product_name = list[i].find('div',class_='p-name p-name-type-2').em.contents[-1]
            # print(product_name)  
            #获取产品价格 
            product_price = list[i].find('div',class_='p-price').i.string
            #获取销量，也就是评价
            product_sale = list[i].find('div',class_='p-commit').a.string
            #取原产地有点问题，尚未解决
            product_num = list[i]['data-sku']
            product_url = 'https://item.jd.com/'+ str(product_num)+'.html'
            print(product_url)
            product_html = getHtmlText(product_url)
            product_provider = parseProduct(product_html)
            print('第'+str(num*30+i+1)+'产品')
            number.append(num*30+i+1) 
            product_flag =list[i]['data-sku']
            flags.append(str(product_flag))
            names.append(product_name)
            prices.append(product_price)
            sale.append(product_sale)
            if product_provider == 0 or product_provider ==-1 or product_provider ==-2:
                exception.append(product_flag)
            provider.append(product_provider)
            # product[i+1] = {'name':product_name,'price':product_price,'sale':product_sale}              
        except:
            count += 1         
            print('出现异常')
         



#########################循环抓取###################################
for i in range(1,101):
    try:
        print('正在抓取第'+str(i)+'页......................')
        url = 'https://search.jd.com/Search?keyword=%E9%98%B2%E8%84%B1%E5%8F%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%98%B2%E8%84%B1%E5%8F%91&stock=1&page='+str(i)+'&s='+str(1+30*(i-1))+'&click=0'
        html = getHtmlText(url)
        parseHtml(html,i-1)
    except:
        pass

########################数据框#################################################
data=pd.DataFrame({'序号':number,"商品编号":flags,"商品名称":names,"价格":prices,"销量":sale,"产地":provider})

#######################保存数据#################################################
data.to_csv('./output/output1.csv',sep=',',index=False,encoding='utf-8')
# data.to_csv('E:\\淘宝爬虫\\output.csv',sep=',',index=False,encoding='gb2312')
with open('./output/exception1.csv','w+') as f:
    for i in range(len(exception)):
        print(exception[i],end='\n',file=f)
######################打印时间和异常值############################################
print('异常值个数：',count)
time2 = time.time()
print(u'ok,爬虫结束!')
print(u'总共耗时：' + str(time2 - time1) + 's')
