# coding=utf-8
import csv
csv_reader = csv.reader(open( r"E:\\淘宝爬虫\\output.csv", encoding='utf-8'))
out = open(r'E:\\淘宝爬虫\\2.csv','w',newline='')              #设置newline，要不然两行之间会空一行
csv_write = csv.writer(out,dialect='excel')     #编码风格，默认是excel
for row in csv_reader:
    csv_write.writerow(row)