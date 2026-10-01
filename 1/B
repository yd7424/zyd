import sys
import re
import json
sys.path.append("..")
from base.spider import Spider

class Spider(Spider):
    def init(self, extend=""):
        # ==========这里修改网站主页==========
        self.siteUrl = "https://wxts.wuxiants850.com/"
        # 多组Headers备用，自动轮流尝试
        self.headersList = [
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                "Referer": self.siteUrl
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": self.siteUrl
            },
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Referer": self.siteUrl
            }
        ]
        # 【多搜索地址模板，{key}是关键词占位】可继续添加
        self.searchUrlList = [
            self.siteUrl + "/search?kw={key}",
            self.siteUrl + "/index.php?s=vod-search-wd-{key}",
            self.siteUrl + "/vodsearch/-------------.html?wd={key}"
        ]
        # 【多分页模板，{page}页码占位】
        self.pageUrlList = [
            "{cid}?page={page}",
            "{cid}/page/{page}/",
            "{cid}-{page}.html"
        ]
        # 多套正则规则集合，可继续新增
        self.rule_cat = [
            re.compile(r'<a href="(.*?)">(.*?)</a>'),
            re.compile(r'class="category" href="(.*?)">(.*?)</span>'),
        ]
        self.rule_list = [
            re.compile(r'<a class="vod-item" href="(.*?)">(.*?)</a>'),
            re.compile(r'<div class="item"><a href="(.*?)">(.*?)</a>'),
            re.compile(r'<li><a href="(.*?)".*?>(.*?)</a></li>'),
        ]
        self.rule_play = [
            re.compile(r'url:"(.*?\.m3u8)"'),
            re.compile(r'src="(.*?\.m3u8)"'),
            re.compile(r'playurl\s*=\s*[\'"](.*?)[\'"]'),
            re.compile(r'var\s+video_url\s*=\s*[\'"](.*?)[\'"]'),
        ]

    # 文本清理函数：去除换行、空格、制表符
    def cleanText(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # 自动尝试多正则，返回匹配结果
    def tryMatch(self, html, ruleList):
        for rule in ruleList:
            res = rule.findall(html)
            if res:
                return res
        return []

    # 循环headers获取页面，哪个成功返回html
    def fetchWithHeaders(self, url):
        for headers in self.headersList:
            resp = self.fetch(url, headers=headers)
            if resp:
                return resp
        return ""

    # 获取分类
    def getCategory(self):
        html = self.fetchWithHeaders(self.siteUrl)
        raw = self.tryMatch(html, self.rule_cat)
        ret = []
        for url,name in raw:
            name = self.cleanText(name)
            ret.append({"type_id":url,"type_name":name})
        return ret

    # 分类影片列表：循环尝试多种分页格式
    def getContent(self, cid, page):
        html = ""
        for pageTpl in self.pageUrlList:
            # 拼接分类地址+分页模板
            pagePath = pageTpl.format(cid=cid, page=page)
            if pagePath.startswith("http"):
                pageUrl = pagePath
            else:
                pageUrl = self.siteUrl + "/" + pagePath.lstrip("/")
            html = self.fetchWithHeaders(pageUrl)
            raw = self.tryMatch(html, self.rule_list)
            if raw:
                ret = []
                for url,name in raw:
                    name = self.cleanText(name)
                    ret.append({"vod_id":url,"vod_name":name})
                return ret
        # 所有分页规则都匹配失败返回空
        return []

    # 搜索影片：循环尝试多个搜索地址
    def searchContent(self, key, page):
        html = ""
        for urlTpl in self.searchUrlList:
            searchUrl = urlTpl.format(key=key)
            html = self.fetchWithHeaders(searchUrl)
            raw = self.tryMatch(html, self.rule_list)
            if raw:
                ret = []
                for url,name in raw:
                    name = self.cleanText(name)
                    ret.append({"vod_id":url,"vod_name":name})
                return ret
        return []

    # 获取播放地址
    def getDetail(self, vid):
        html = self.fetchWithHeaders(f"{self.siteUrl}/{vid}")
        raw = self.tryMatch(html, self.rule_play)
        playUrl = raw[0] if raw else ""
        return {"vod_play_url": playUrl}