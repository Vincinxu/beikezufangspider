import requests
from requests.exceptions import RequestException
import pymysql
from bs4 import BeautifulSoup



class JdSpider():
    def __init__(self, keyword, max_page, mysql_host,
                 mysql_user, mysql_password, mysql_db, mysql_port):
        self.keyword = keyword
        self.max_page = max_page
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.mysql_port = mysql_port

    def get_page(self, page):
        try:
            url = 'https://' + self.keyword + '.zu.ke.com/zufang/pg' + str(page)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None

    def parse_page(self, html):
        bs = BeautifulSoup(html, 'lxml')
        items = bs.select('.content__list .content__list--item')
        for item in items:
            product = {
                'image': item.select('.content__list--item--aside img')[0].attrs['data-src'],
                'title': item.select('.content__list--item--title')[0].get_text().replace('\n', '').strip(),
                'description': item.select('.content__list--item--des')[0].get_text().replace('\n', '').replace(' ', '').strip(),
                'tag': item.select('.content__list--item--bottom')[0].get_text().replace('\n', ' '),
                'brand': item.select('.content__list--item--brand')[0].get_text().replace(' ', '').replace('\n', ' ').strip(),
                'price': item.select('.content__list--item-price')[0].get_text()
            }
            yield product


    def save_to_mysql(self, content):
        self.db = pymysql.connect(self.mysql_host, self.mysql_user, self.mysql_password,
                                  self.mysql_db, self.mysql_port, charset='utf8')
        cursor = self.db.cursor()
        table = 'bk'
        data = dict(content)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (table, keys, values)
        cursor.execute(sql, tuple(data.values()))
        self.db.commit()

    def close_sql(self):
        self.db.close()


    def run(self):
        for i in range(1, self.max_page + 1):
            html = self.get_page(i)
            content = self.parse_page(html)
            for item in content:
                self.save_to_mysql(item)
                print(item)
        self.close_sql()



if __name__ == '__main__':
    JdSpider('gz', 100, 'localhost', 'root', '12345', 'beike', 3306).run()