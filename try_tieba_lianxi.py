# coding = utf8
import requests


class TiebaSpider():

    def __init__(self,tieba_name):
        self.tieba_name = tieba_name
        self.headers={
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
       }
    def get_url_list(self):
        url_list=[]
        #构造每一页的url
        for i in range(1000):
            url_temp = 'https://tieba.baidu.com/f?kw='+self.tieba_name+"&ie= utf-8&pn={}".format(i*50)
            url_list.append(url_temp)
        return url_list

    def parse_url(self,url):
        """解析url"""
        print("now parsing",url)
        response = requests.get(url,headers=self.headers)
        return response.content.decode()
    def save_html(self,html_str,page_num):
        """保存页面"""
        file_path = self.tieba_name+"_第"+str(page_num)+"页.html"
        # 保存路径方式:贴吧名+页码.html
        with open(file_path,"w",encoding="utf8")as f:
            # 文件打开方式(文件名,写入,编码格式) 代号f
            f.write(html_str)
            # 调用写方法将html_str写入
            print("save success")

    def run(self):
        # 1. 找到url的规律,构造url_list

        url_list=self.get_url_list()
        # 2. 遍历url list ，发送请求，获取响应
        for url in url_list:
            # 3.提取html str，
            html_str = self.parse_url(url)
            # 4.保存
            page_num=url_list.index(url)+1
            self.save_html(html_str,page_num)
if __name__ =="__main__":
    tieba_spider = TiebaSpider("电影")
    tieba_spider.run()

