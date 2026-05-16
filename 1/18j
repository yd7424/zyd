# coding=utf-8   
 #!/usr/bin/python   
 import sys   
 import base64   
 import re   
 import json  
 sys.path.append("..")   
 from base.spider import Spider   
  
 class Spider(Spider):   
     def getName(self):   
         return "18J-夜明空"   
  
     def init(self, extend=""):   
         pass   
  
     def isVideoFormat(self, url):   
         pass   
  
     def manualVideoCheck(self):   
         pass   
  
     def action(self, action):   
         pass   
  
     def destroy(self):   
         pass   
  
     # 1. 替换基础网址和请求头 
     host = "https://18oc.life"  
     headers = {   
         'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041211AC Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36',  
         'Referer': 'https://18oc.life/',  
         'Accept': '*/*',  
         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',  
         'Connection': 'keep-alive'  
     }   
  
     def homeContent(self, filter):   
         result = {}   
         classes = []   
         cateManual = {}   
  
         # 2. 替换为 18J 的完整分类映射 
         cateManual = {   
             "最新": "/label/hot/by/time/page/{pg}/", 
             "日榜": "/label/hot/by/hits_day/page/{pg}/", 
             "周榜": "/label/hot/by/hits_week/page/{pg}/", 
             "月榜": "/label/hot/by/hits_month/page/{pg}/", 
             "国产": "/t/1-{pg}/", 
             "国产 - 自拍": "/t/5-{pg}/", 
             "国产 - 探花": "/t/7-{pg}/", 
             "国产 - 偷拍": "/t/8-{pg}/", 
             "国产 - 吃瓜": "/t/10-{pg}/", 
             "日韩": "/t/2-{pg}/", 
             "日韩 - 日本无码": "/t/14-{pg}/", 
             "日韩 - 字幕": "/t/15-{pg}/", 
             "欧美": "/t/3-{pg}/", 
             "动漫": "/t/16-{pg}/", 
             "伦理": "/t/4-{pg}/", 
             "另类": "/t/39-{pg}/" 
         }   
  
         for k in cateManual:   
             # 这里的 type_id 直接存分类的路径模板 
             classes.append({ 
                 'type_name': k,    
                 'type_id': cateManual[k] 
             })   
  
         result['class'] = classes   
         return result   
  
     def homeVideoContent(self):   
         pass   
  
     def categoryContent(self, tid, pg, filter, extend):   
         result = {}   
         # 3. 适配 18J 的分类链接拼接逻辑 
         # tid 就是我们在 homeContent 里存的 "/t/1-{pg}/" 这种模板 
         path = tid.replace("{pg}", pg) 
         url = self.host + path   
  
         data = self.fetch(url, headers=self.headers).text   
         videos = self.get_list(data)   
         result['list'] = videos   
         result['page'] = pg   
         result['pagecount'] = 9999   
         result['limit'] = 90   
         result['total'] = 999999   
         return result   
  
     def detailContent(self, ids):   
         url = self.host + ids[0] if not ids[0].startswith('http') else ids[0]   
         data = self.fetch(url, headers=self.headers).text   
  
         # 获取当前视频的基本信息（标题、封面等） 
         videos = self.get_list(data)   
         vod = videos[0] if videos else {"vod_id": ids[0], "vod_name": "未知影片", "vod_pic": "", "vod_remarks": ""}   
  
         from_arr = ["18J-直连"]  
         url_arr = []  
  
         # 4. 核心修改：提取 18J 的真实 m3u8/mp4 播放地址 
         try:  
             # 匹配网页源码中的 source = "https://...m3u8" 或 source = '...mp4' 
             match = re.search(r'source\s*=\s*["\']([^"\']*?\.(?:m3u8|mp4)[^"\']*)["\']', data, re.IGNORECASE) 
             if match:  
                 real_video_url = match.group(1).replace('\\/', '/').replace('\\', '') 
                 # 直接把真实的视频地址作为播放链接 
                 url_arr.append("立即播放$" + real_video_url)  
                 print("成功提取真实播放地址:", real_video_url)  
         except Exception as e:  
             print("提取真实播放地址失败:", e)  
  
         # 如果正则没提取到，走保底逻辑（提取页面上的其他播放列表） 
         if not url_arr:  
             print("未提取到真实地址，尝试保底提取播放页链接...")  
             li_groups = re.findall(r'<ul[^>]*class="[^"]*content_playlist[^"]*"[^>]*>(.*?)</ul>', data, re.S)   
             if li_groups:   
                 for group in li_groups:   
                     li_items = re.findall(r'<li[^>]*><a[^>]*href="([^"]*)"[^>]*>(.*?)</a></li>', group, re.S)   
                     ep_str = ""   
                     for li in li_items:   
                         name = li[1].replace(" ", "").replace("\n", "").replace("\t", "")   
                         if name and li[0]:   
                             ep_str += name + "$" + li[0] + "#"   
                     if ep_str:   
                         url_arr.append(ep_str.rstrip('#'))   
  
         vod['vod_play_from'] = "$$$".join(from_arr)   
         vod['vod_play_url'] = "$$$".join(url_arr)   
         result = {'list': [vod]}   
         return result   
  
     def searchContent(self, key, quick, pg="1"):   
         videos = []   
         # 5. 适配 18J 的搜索链接 
         url = self.host + '/s/page/' + pg + '/wd/' + key + '/' 
         try:   
             res = self.fetch(url, headers=self.headers)   
             if res.text and '没有找到' not in res.text:   
                 videos = self.get_list(res.text)   
         except Exception as e:  
             print("搜索请求异常:", e)  
  
         result = {'list': videos, 'page': pg}   
         return result   
  
     def playerContent(self, flag, id, vipFlags):   
         # 因为 detailContent 里已经是真实地址了，这里直接返回即可  
         result = {}   
         result['parse'] = 0   
         result['url'] = id   
         result['header'] = self.headers   
         return result   
  
     def get_list(self, html):   
         videos = []   
         # 6. 核心修改：适配 18J 的列表页 HTML 结构提取正则 
         # 18J 的列表通常是 <a href="/v/xxx.html" title="标题"> <img data-original="封面"> 
         items = re.findall(r'<a[^>]*href="(/v/[^"]*)"[^>]*title="([^"]*)"[^>]*>.*?<img[^>]*(?:data-original|src)="([^"]*)"', html, re.S)   
  
         for item in items:   
             videos.append({   
                 "vod_id": item[0],  # 存相对路径，如 /v/123.html 
                 "vod_name": item[1],   
                 "vod_pic": item[2] if item[2] else "",   
                 "vod_remarks": ""   
             })   
         return videos   
  
     localdata = {}
