import sys
import re
import json
from urllib.parse import quote
sys.path.append("..")
from base.spider import Spider

class Spider(Spider):
    def init(self, extend=""):
        self.siteUrl = "https://wxts.wuxiants850.com"
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
        self.searchUrlList = [
            self.siteUrl + "/search?kw={key}",
            self.siteUrl + "/index.php?s=vod-search-wd-{key}",
            self.siteUrl + "/vodsearch/-------------.html?wd={key}"
        ]
        self.pageUrlList = [
            "{cid}?page={page}",
            "{cid}/page/{page}/",
            "{cid}-{page}.html"
        ]
        self.rule_cat = [
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

    def cleanText(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def tryMatch(self, html, ruleList):
        for rule in ruleList:
            res = rule.findall(html)
            if res:
                return res
        return []

    def fetchWithHeaders(self, url):
        for headers in self.headersList:
            resp = self.fetch(url, headers=headers)
            if resp:
                return resp
        return ""

    def getCategory(self):
        html = self.fetchWithHeaders(self.siteUrl)
        raw = self.tryMatch(html, self.rule_cat)
        ret = []
        for url,name in raw:
            name = self.cleanText(name)
            ret.append({"type_id":url,"type_name":name})
        return ret

    def getContent(self, cid, page):
        html = ""
        for pageTpl in self.pageUrlList:
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
        return []

    def searchContent(self, key, page):
        html = ""
        key_encode = quote(key)
        for urlTpl in self.searchUrlList:
            searchUrl = urlTpl.format(key=key_encode)
            html = self.fetchWithHeaders(searchUrl)
            raw = self.tryMatch(html, self.rule_list)
            if raw:
                ret = []
                for url,name in raw:
                    name = self.cleanText(name)
                    ret.append({"vod_id":url,"vod_name":name})
                return ret
        return []

    def getDetail(self, vid):
        if vid.startswith("http"):
            url = vid
        else:
            url = f"{self.siteUrl}/{vid}"
        html = self.fetchWithHeaders(url)
        raw = self.tryMatch(html, self.rule_play)
        playUrl = raw[0] if raw else ""
        if playUrl:
            playUrl = f"播放${playUrl}"
        return {"vod_play_url": playUrl}
