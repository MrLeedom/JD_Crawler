# CrowTaobaoPrice.py
import requests
import re
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        llt = re.findall(r'\"item_loc\"\:\".*?\"', html)
        print(plt)
        print(tlt)
        print(llt)
        for i in range(len(tlt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            loc = eval(llt[i].split(':')[1])
            ilt.append([price,loc,title])
    except:
        print("")
def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}\t{:8}"
    print(tplt.format("序号", "价格", "发货地", "产品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1], g[2]))
def main():
    goods = 'gtx1060'
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' + goods
#     start_url = 'http://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=869f54c152fd0457c7150c5a0c6fdc90&keyword=gtx1060&page=0'
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
        #     url = 'http://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=869f54c152fd0457c7150c5a0c6fdc90&keyword=gtx1060&page=0'
            html = getHTMLText(url)

            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)
main()
