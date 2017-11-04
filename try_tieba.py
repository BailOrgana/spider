# coding= utf8
import requests


class  TiebaSpider:
    def __init__(self,tieba_name):
        self.tieba_name=tieba_name
        self.headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }


    #1.找到url规律，构造url list
    def get_url_list(self):
        url_list= []
        for i in range (1000):
            url_temp= "https://tieba.baidu.com/f?kw="+self.tieba_name+"&ie=utf-8&pn={}".format(i*50)
            url_list.append(url_temp)
        return url_list

    # 2. 遍历url list ，发送请求，获取响应
    def parse_url(self,url):
        print('now parsing',url)
        response = requests.get(url,headers=self.headers,)
        return response.content.decode()
    # 3.提取html str，
    # 4.保存
    def save_html(self,html_str,page_number):
        file_path = self.tieba_name+"_第"+str(page_number)+"页.html"
        with open(file_path,"w",encoding="utf-8") as f:
            f.write(html_str)
            print("save success")

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            html_str = self.parse_url(url)
            page_number =url_list.index(url)+1
            self.save_html(html_str,page_number)


if __name__ == '__main__':
    tieba_spider = TiebaSpider("李毅")
    tieba_spider.run()