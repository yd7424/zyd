if (typeof Object.assign !== 'function') {
     Object.assign = function () {
         let target = arguments[0];
         for (let i = 1; i < arguments.length; i++) {
             let source = arguments[i];
             for (let key in source) {
                 if (Object.prototype.hasOwnProperty.call(source, key)) {
                     target[key] = source[key];
                 }
             }
         }
         return target;
     };
 }
 let common_lazy = `js:
   let html = request(input);
   // 修正正则，精准匹配 var player_aaaa={...}
   let reg = /var player_aaaa=(\\{.+?\\})/;
   let matchRes = html.match(reg);
   if(!matchRes) return input;
   let json = JSON5.parse(matchRes[1]);
   let url = json.url;
   if (json.encrypt == '1') {
     url = unescape(url);
   } else if (json.encrypt == '2') {
     url = unescape(base64Decode(url));
   }
   if (/\\.(m3u8|mp4|m4a|mp3)/.test(url)) {
     input = {
       parse: 0,
       jx: 0,
       url: url,
     };
   } else {
     input = url && url.startsWith('http') && tellIsJx(url) ? {parse:0,jx:1,url:url}:input;
   }`;
var rule = {
     title: '里面(满血版)',
     host: 'https://baf7baf7.shewo11.cc',
     url: '/vodtype/fyclass-fypage.html',
     filterable: 0,
    class_name: '国产精品&华语精品&黑料吃瓜&欧美大尺&动漫禁漫&学生合集&乱伦精品&探花约炮&日本无码&日本有码&主播网红&国产色情&自拍偷拍&人妻熟女&黑人洋屌&欧美精品&卡通动漫&乱伦中文&传媒原创&口爆颜射&韩国女优&萝莉少女&重口调教&国产直播&韩国群交&中文字幕&吃瓜爆料&角色扮演&熟女自慰&韩国直播&公开漏出&户外打炮',
class_url: '55&63&58&60&57&65&64&61&86&80&81&12&21&22&23&24&69&70&71&72&25&26&88&56&73&75&76&77&78&84&85&89',
    searchUrl: '/vodsearch/-------------.html?wd=**',
     searchable: 1,
     quickSearch: 0,
     headers: {
         'User-Agent': 'Mozilla/5.0 (Linux; Android 9) Mobile Safari/537.36'
     },
     lazy: common_lazy,
     limit: 6,
     double: true,
     // 修复一级列表标准分段语法：容器;标题;图片;简介;链接
     // 1. 一级解析（列表页）
// 格式规范：列表容器;标题;图片;描述;链接;详情(可选)
一级: '.pornkvideos;a&&title;img&&data-src;.vlength&&Text;a&&href',

// 2. 二级解析（详情页）
二级: {
    title: '.htitle&&Text',
    img: '.video-img&&data-src',
    desc: '.video_cats a&&Text',
    content: '', // 如果不需要简介，留空即可
    tabs: '#playerr', // 播放源标签的容器
    lists: '#playerr', // 播放列表的容器
    tab_text: 'body&&Text', // 【关键修复】提取标签文字的规则
    list_text: 'a&&Text',   // 【关键补充】提取集数名称的规则
    list_url: 'a&&href'     // 【关键补充】提取集数链接的规则
},
     搜索: '.pornkvideos;a&&title;img&&data-src;.vlength&&Text;a&&href',
     linkPrefix: 'https://baf7baf7.shewo11.cc',
sniff: {
         enable: 0
     }
 };
 return rule;