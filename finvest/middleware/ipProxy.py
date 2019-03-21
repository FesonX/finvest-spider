import requests
from scrapy.selector import Selector
import pymysql
import time

conn = pymysql.connect(host="127.0.0.1", user="feson", passwd="feson", db="Spider", charset="utf8")
cursor = conn.cursor()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


class GetRandomIp(object):
    def parse(self, next_url='/inha/1'):
        """
        Parse Ip List From Site, Transfer to parse_detail
        :param next_url:
        :return: None
        """
        print("Begin Parsing...")
        response = requests.get(url='https://www.kuaidaili.com/free/intr'.format(next_url), headers=headers)
        response = Selector(text=response.text)
        tr_list = response.xpath('//*[@id="list"]/table/tbody/tr/td')
        if tr_list:
            self.parse_detail(tr_list)

        for i in range(20):
            time.sleep(5)
            next_url = 'https://www.kuaidaili.com/free/intr/%d' % i
            if next_url:
                self.parse(next_url)

    def parse_detail(self, tr_list):
        """
        Parse Ip detail from list, transfer to insert into database
        :param tr_list:
        :return: None
        """
        ip = tr_list.xpath('//td[@data-title="IP"]/text()').extract()
        port = tr_list.xpath('//td[@data-title="PORT"]/text()').extract()
        type = tr_list.xpath('//td[@data-title="类型"]/text()').extract()
        speed = tr_list.xpath('//td[@data-title="响应速度"]/text()').extract()

        for i in range(len(ip)):
            self.insert_sql(ip[i], port[i], type[i])

    def insert_sql(self, ip, port, type):
        type = type.lower()
        proxy_url = '{0}://{1}:{2}'.format(type, ip, port)
        res = self.check_ip(type, proxy_url)
        print(proxy_url)
        if res:
            cursor.execute(
                "insert proxy_ip(ip, port, type) VALUES('{0}', '{1}', '{2}')".format(
                    ip, port, type
                )
            )
            conn.commit()

    def get_ip(self):
        sql = "select * from proxy_ip ORDER BY RAND() LIMIT 1"
        cursor.execute(sql)
        ip, port, type = cursor.fetchone()
        conn.commit()

        type = type.lower()
        proxy_url = '{0}://{1}:{2}'.format(type, ip, port)
        res = self.check_ip(type, proxy_url)
        if res:
            return proxy_url
        else:
            self.delete_ip(ip)
            return self.get_ip()

    def check_ip(self, type, proxy_url):
        request_url = 'http://hf.58.com/ershoufang/0'
        try:
            proxy = {type: proxy_url}
            response = requests.get(url=request_url, proxies=proxy, timeout=5)
        except Exception as e:
            print(e)
            return False
        else:
            code = response.status_code
            if code == 200 or code == 302:
                return True
            else:
                print('invalid ip and port')
                return False

    def delete_ip(self, ip):
        sql = """delete from proxy_ip where ip='%s'""" %  ip
        cursor.execute(sql)
        conn.commit()


ip = GetRandomIp()

if __name__ == '__main__':
    ip = GetRandomIp()
    ip.parse()
    # print(ip.get_ip())
