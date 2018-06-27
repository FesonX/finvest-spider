# finvest-spider
Finance and Investment Info Spider Collections - 投融资信息爬取集合
>取Finance和Investment的前几个字母组成项目名

## 已接入爬虫的网站
>### [投中网](www.chinaventure.com.cn)
Spider名称: trjcn

>### [投融界](http://news.trjcn.com/list_70.html)
Spider名称: cvnews


## 常用的爬虫命令
>1. 爬取并输出csv文件
```shell
scrapy crawl [spider_name] -o [doc_name].csv
```
>2. 爬取N页停止
```shell
scrapy crawl [spider_name] -s CLOSESPIDER_PAGECOUNT=[N]
```
>3. 爬取N项停止
```shell
scrapy crawl [spider_name] -s CLOSESPIDER_ITEMCOUNT=[N]
```
>4. 超时停止
```shell
scrapy crawl [spider_name] -s CLOSESPIDER_TIMEOUT=[N]
```

## LICENSE
[MIT](/LICENSE)