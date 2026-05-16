import sys 
import base64 
import re 
import json
sys.path.append("..") 
from base.spider import Spider 
class Spider(Spider):
    def init(self, extend=""):
        pass 
host = "https://bnk.yzfnb2.makeup"

headers = { 
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Referer': 'https://bnk.yzfnb2.makeup/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
} 

def homeContent(self, filter):
    result = {}
    cateManual = {
        "熟母少妇": "/cn/home/web/index.php/vod/type/id/20.html",
        "网红直播": "/cn/home/web/index.php/vod/type/id/21.html",
        "自拍偷拍": "/cn/home/web/index.php/vod/type/id/22.html",
        "强奸乱伦": "/cn/home/web/index.php/vod/type/id/23.html",
        "高清国产": "/cn/home/web/index.php/vod/type/id/24.html",
        "韩国专区": "/cn/home/web/index.php/vod/type/id/25.html",
        "日本有码": "/cn/home/web/index.php/vod/type/id/26.html",
        "日本无码": "/cn/home/web/index.php/vod/type/id/27.html",
        "欧美情色": "/cn/home/web/index.php/vod/type/id/28.html",
        "动漫卡通": "/cn/home/web/index.php/vod/type/id/29.html",
        "三级伦理": "/cn/home/web/index.php/vod/type/id/30.html"
    }

    classes = []
    for k in cateManual:
        classes.append({'type_name': k, 'type_id': cateManual[k]})
        
    result['class'] = classes
    return result

def categoryContent(self, tid, pg, filter, extend):
    result = {}
    videos = []
    try:
        url = self.host + tid
        if pg != '1':
            url = tid.replace('.html', '-' + str(pg) + '.html')
            url = self.host + url

        res = self.fetch(url, headers=self.headers)
        videos = self.get_list(res.text)
    except Exception as e:
        print("获取分类影片失败:", e)
        
    result['list'] = videos
    result['page'] = pg
    result['pagecount'] = 9999  
    result['limit'] = 90
    result['total'] = 999999
    return result

# 【精准修复版】详情页与播放地址提取
def detailContent(self, array):
    ids = array
    vod_id = ids[0]
    url = self.host + vod_id if not vod_id.startswith('http') else vod_id
    data = self.fetch(url, headers=self.headers).text 
    
    vod = {"vod_id": vod_id, "vod_name": "未知影片", "vod_pic": "", "vod_remarks": ""}

    # 根据你提供的HTML源码，进行绝对精准的提取
    try:
        # 1. 提取真实片名：直接在 <h3> 标签里抓取
        name_match = re.search(r'<h3>([^<]+)</h3>', data)
        if name_match:
            vod["vod_name"] = name_match.group(1).strip()

        # 2. 提取备注信息：在 h3 下面的 div.videoplay_btnwrap 里（如：播放7次，2026-05-11）
        remark_match = re.search(r'<div class="videoplay_btnwrap">\s*([^<]+)', data)
        if remark_match:
            vod["vod_remarks"] = remark_match.group(1).strip()

        # 3. 提取海报图片：优先匹配 player_data 里的封面，其次匹配 img 标签
        pic_match = re.search(r'"pic":"([^"]*)"', data) or re.search(r'<img[^>]*(?:data-original|src)="([^"]*)"', data)
        if pic_match:
            vod["vod_pic"] = pic_match.group(1)

    except Exception as e:
        print("提取详情页基础信息出错:", e)
    
    url_arr = []
    from_arr = ["默认线路"]

    # 核心提取逻辑：匹配源码中的真实 m3u8 地址
    try:
        player_data_match = re.search(r'var player_data=(\{.*?\})', data, re.S)
        if player_data_match:
            player_json = json.loads(player_data_match.group(1))
            real_video_url = player_json.get('url', '')
            encrypt_type = player_json.get('encrypt', 0)
            
            if real_video_url:
                # 识别明文 m3u8 直链，加上 proxy:// 前缀直接放行
                if encrypt_type == 0 and '.m3u8' in real_video_url:
                    final_play_url = 'proxy://' + real_video_url
                else:
                    final_play_url = real_video_url
                
                url_arr.append("立即播放$" + final_play_url)
    except Exception:
        pass
    
    # 保底逻辑：提取普通跳转链接
    if not url_arr:
        li_groups = re.findall(r'<ul[^>]*class="[^"]*content_playlist[^"]*"[^>]*>(.*?)</ul>', data, re.S) 
        if li_groups: 
            for group in li_groups: 
                li_items = re.findall(r'<li[^>]*><a[^>]*href="([^"]*)"[^>]*>(.*?)</a></li>', group, re.S) 
                ep_str = "" 
                for li in li_items: 
                    name = li[1].strip()
                    if name and li[0]: 
                        ep_str += name + "$" + li[0] + "#" 
                if ep_str: 
                    url_arr.append(ep_str.rstrip('#')) 

    vod['vod_play_from'] = "$$$".join(from_arr) 
    vod['vod_play_url'] = "$$$".join(url_arr) 
    return {'list': [vod]} 

def searchContent(self, key, quick, pg="1"):
    url = self.host + '/cn/home/web/index.php/vod/search.html' 
    videos = [] 
    try: 
        get_url = url + '?wd={}&page={}'.format(key, pg) 
        res = self.fetch(get_url, headers=self.headers) 
        videos = self.get_list(res.text)
    except Exception:
        pass
    return {'list': videos} 

def playerContent(self, flag, id, vipFlags): 
    result = {}
    if id.startswith('proxy://'):
        result['parse'] = 0  
        result['url'] = id.replace('proxy://', '')
        result['header'] = self.headers
        return result

    final_url = id 
    try: 
        data = self.fetch(id, headers=self.headers).text 
        hconf = re.search(r'var player_.?=(.*?)<', data) 
        if hconf: 
            conf = json.loads(hconf.group(1)) 
            play_url = conf.get('url', '') 
            encrypt = conf.get('encrypt', 0) 
        
            if encrypt == 0:
                final_url = play_url
            elif encrypt == 1: 
                from urllib.parse import unquote 
                final_url = unquote(play_url) 
            elif encrypt == 2: 
                b64_decoded = base64.b64decode(play_url).decode('utf-8') 
                from urllib.parse import unquote 
                final_url = unquote(b64_decoded)
    except Exception:
        pass

    result['parse'] = 1 
    result['url'] = final_url 
    result['header'] = self.headers 
    return result 

def get_list(self, html): 
    videos = [] 
    items = re.findall(r'<a[^>]href="([^"]*(?:detail|play)[^"]*)"[^>]title="([^"]*)"[^>]*>.*?<img[^>]*(?:data-original|src)="([^"]*)"', html, re.S) 
    for item in items: 
        videos.append({ 
            "vod_id": item[0], 
            "vod_name": item[1], 
            "vod_pic": item[2] if item[2] else "", 
            "vod_remarks": "" 
        }) 
    return videos 

localdata = {}
