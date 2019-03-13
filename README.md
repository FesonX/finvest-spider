# finvest-spider
Finance and Investment Info Spider Collections - 投融资信息爬取集合
>取Finance和Investment的前几个字母组成项目名

## 已接入爬虫的网站
>### [投中网](http://www.chinaventure.com.cn)
Spider名称: trjcn
行业: 综合

>### [投融界](http://news.trjcn.com/list_70.html)
Spider名称: cvnews
行业: 综合

>### [36Kr](https://36kr.com/newsflashes)
Spider名称: 36kr
行业: 综合

>### [动脉网](https://vcbeat.net)
Spider名称: vcbeat
行业: 医疗

>### [芥末堆](https://www.jiemodui.com)
Spider名称: jiemodui
行业: 教育

>### [GAMELOOK](http://www.gamelook.com.cn/)
Spider名称: gamelook
行业: 游戏


## 爬虫分析过程
>[JS动态加载以及JavaScript void(0)的爬虫解决方案](HOW_TO_CRAWL_AboutJS.md)

## 安装依赖软件
>1. [安装MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition)
*注意*:以Deepin为例,如果使用Ubuntu的安装方法报错--`keyserver receive failed: No dirmngr`,请先键入下面命令再使用上方链接的教程
`sudo apt-get install software-properties-common dirmngr`

如果安装完成后遇到
`Failed to start mongod.service: Unit not found`
请参考[文章](https://www.cnblogs.com/alan2kat/p/7771635.html)

>2. 安装Python
```shell
# For Ubuntu/Deepin etc.
apt-get install python3
```

>3. 安装库依赖
有关虚拟环境内容, 自行 Google `Virtualenv`
`pip install -r requirements.txt`


## 常用的爬虫命令
>1. 爬取并输出csv文件
本项目默认输出 csv 文件, 关于输出的 pipeline 请参考 `pipeline.py` 中的相关类
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
请移步 `data` 文件夹.
仅供学习用途, 请勿商用.

## LICENSE
[MIT](/LICENSE)