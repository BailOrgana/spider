# coding = utf8
import  requests
from retrying import retry
from lxml import etree
import json

class TiebaSPider:
    def __init__(self,tieba_name):
        self.tieba_name=tieba_name
        # 1.start_url 首页的url地址
        self.part_url = "http://tieba.baidu.com/mo/q---416E9FE6A1C5203A16807F0FD4FCC847%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1507618417878_84/"
        self.strat_url="http://tieba.baidu.com/mo/q---416E9FE6A1C5203A16807F0FD4FCC847%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1507618417878_84/m?kw={}&lp=5011&lm=&pn=0".format(tieba_name)
        self.headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }

    @retry(stop_max_attempt_number=4)
    def _parse_url(self,url):
        r = requests.get(url,headers=self.headers,timeout=5)
        assert r.status_code==200
        return etree.HTML(r.content)
    def parse_url(self,url):
        print(url)
        try:
            html = self._parse_url(url)
        except:
            html = None
        return html
    def get_content_list(self,html):
        div_list = html.xpath("//div[contains(@class,'i')]")
        content_list=[]
        for div in div_list:
            item={}
            item["href"]=self.part_url+div.xpath("./a/@href")[0] if len(div.xpath("./a/@href"))>0 else None
            item["title"]=div.xpath("./a/text()")[0] if len(div.xpath("./a/text()"))>0 else None
            content_list.append(item)
        next_url_temp=html.xpath("//a[text()='下一页']/@href")
        next_url =self.part_url+next_url_temp[0] if len(next_url_temp)>0 else None
        return content_list,next_url
    def get_imp_list(self,href):
        # 5.获取帖子里面的图片
        html_detail = self.parse_url(href)
        img_list =html_detail.xpath("//img[@class='BDE_Image']/@src")
        img_list = [requests.utils.unquote(i).split("src=")[-1] for i in img_list]
        return img_list
    def save_content_list(self,content_list):
        with open(self.tieba_name+'.txt',"a") as f:
            for content in content_list:
                f.write(json.dumps(content,ensure_ascii=False,indent=2))
                f.write("\n")
        print("保存成功")




    def run(self):
        # 1.start_url 首頁的url地址
        next_url = self.start_url
        # 解析,發送請求,獲取響應
        while next_url is not None:
            html = self.parse_url(next_url)
        #提取數據,title,href,下一頁的url
            content_list,next_url=self.get_content_list(html)
            # 4.遍历发送帖子href的请求，
            for content in content_list:
                href = content["href"]
                # 5.获取帖子里面的图片
                content["img_list"]=self.get_img_list(href)
            self.save_content_list(content_list)
if __name__ == '__main__':
    tieba = TiebaSPider("李毅")
    tieba.run()
