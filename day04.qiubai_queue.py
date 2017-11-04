# coding= utf8
import requests
import json
from retrying import retry
from queue import Queue
import threading
from lxml import etree


class QiuBai:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        self.url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_list_queue = Queue()

    def get_url_list(self):
        url_list = [self.url_temp.format(i) for i in range(1, 14)]
        for url in url_list:
            self.url_queue.put(url)

    @retry(stop_max_attempt_number=4)
    def _parse_url(self, url, return_str=False):
        r = requests.get(url, headers=self.headers, timeout=5)
        assert r.status_code == 200
        return etree.HTML(r.content)

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print(url)
            try:
                html = self._parse_url(url)
            except:
                html = None
            self.html_queue.put(html)
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            html = self.html_queue.get()
            if html is not None:
                div_list = html.xpath("//div[@id='content-left']/div")
                content_list = []
                for div in div_list:
                    item = {}
                    item["username"] = div.xpath(".//h2/text()")[0].replace("\n", "") if len(
                        div.xpath(".//h2/text()")) > 0 else None
                    item["content"] = div.xpath(".//div[@class='content']/span/text()")
                    item["content"] = [i.replace("\n", "") for i in item["content"]]
                    item["img_list"] = div.xpath(".//span[@class='thumb']/a/img/@src")
                    item["stats_vote"] = div.xpath(".//span[@class='stats-vote']/i/text()")
                    item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"]) > 0 else None
                    item["user_gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
                    item["user_gender"] = item["user_gender"][0].split(" ")[-1] if len(
                        item["user_gender"]) > 0 else None
                    content_list.append(item)
                self.content_list_queue.put(content_list)
            self.html_queue.task_done()
                    # 配合get计数减少1

    def save_content_list(self):
        while True:
            content_list = self.content_list_queue.get()
            with open("qiubai.txt", "a")as f:
                for content in content_list:
                    json.dump(content, f, ensure_ascii=False, indent=2)
                    f.write("\n")
            self.content_list_queue.task_done()

    def run(self):

        # 1.url list
        thread_list = []
        # url_list = self.get_url_list()
        t_url = threading.Thread(
            target=self.get_url_list
        )
        thread_list.append(t_url)
        # 2遍历，发送请求，获取响应
        for i in range(1):
            t_parse = threading.Thread(
                target=self.parse_url
            )
            thread_list.append(t_parse)
        # 3.提取数据
        for i in range(3):
            t_get_content_list = threading.Thread(target=self.get_content_list)
            thread_list.append(t_get_content_list)
        # 4.保存
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)
        for t in thread_list:
            t.setDaemon(True)  # 设置守护线程，说明该线程不重要，主线程结束，子线程结束
            t.start()
        for q in [self.url_queue, self.html_queue, self.content_list_queue]:
            q.join()  # 等待，让主线程等待，队列计数为0之后才会结束，否则会一直等待


if __name__ == '__main__':
    qiubai = QiuBai()
    qiubai.run()
