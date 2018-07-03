# finvest-spider
Finance and Investment Info Spider Collections - 投融资信息爬取集合
>取Finance和Investment的前几个字母组成项目名

## 已接入爬虫的网站
>### [投中网](http://www.chinaventure.com.cn)
Spider名称: trjcn

>### [投融界](http://news.trjcn.com/list_70.html)
Spider名称: cvnews


## 安装依赖软件
>1. [安装MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition)
*注意*:以Deepin为例,如果使用Ubuntu的安装方法报错--`keyserver receive failed: No dirmngr`,请先键入下面命令再使用上方链接的教程
`sudo apt-get install software-properties-common dirmngr`

如果安装完成后遇到
`Failed to start mongod.service: Unit not found`
请参考[文章](https://www.cnblogs.com/alan2kat/p/7771635.html)

>2. 安装Python

>3. 安装库依赖


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

## 数据示例
>1. [投中网](/finvest/cvnews.csv)
>2. [投融界](/finvest/trjcn.csv)

## LICENSE
[MIT](/LICENSE)