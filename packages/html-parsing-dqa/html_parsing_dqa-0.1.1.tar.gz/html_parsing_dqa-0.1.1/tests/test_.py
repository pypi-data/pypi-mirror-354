import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from html_parsing.feild_extraction import *



class Test(unittest.TestCase):

    def setUp(self):
        self.html = """<!doctype html>
<html data-log-pv="{&quot;mpc&quot;:31}">
 <head>
 <title>职场下午茶，如何把握？_领导_奶茶_方式</title>
 <meta http-equiv="Cache-Control" content="no-transform">
 <meta http-equiv="Cache-Control" content="no-siteapp">
 <meta name="copyright" content="Copyright © 2017 Sohu.com Inc. All Rights Reserved.">
 <meta name="mediaid" content="骑着小木马走天下">
 <meta property="og:type" content="news">
 <meta property="og:image" content="//q4.itc.cn/images01/20240104/8d46b4af8f714c66a7ac077f036af0c2.jpeg">
 <meta property="og:url" content="www.sohu.com/a/749607511_121846184">
 <meta property="og:release_date" content="2024-01-04 22:46">
 <meta itemprop="dateUpdate" content="2024-01-04 22:46">
 <meta itemprop="datePublished" content="2024-01-04 22:46">
 <link rel="canonical" href="https://www.sohu.com/a/749607511_121846184">
 <link rel="alternate" media="only screen and(max-width: 640px)" href="m.sohu.com/a/749607511_121846184">
 <meta name="keywords" content="礼仪,职场,关系,单位,领导,是一种,个人,方式,奶茶,行为,礼仪,人际,职场,领导,奶茶">
 <meta name="description" content="在中国的传统文化中，尊重和关心是相互关联的，而表达尊重和关心的方式也有很多种。其次，给领导点奶茶也是一种职场礼仪。在单位里，给领导点奶茶可以视为一种职场礼仪，表示自己对领导的尊重和关心，同时也是一种表示礼貌和…">
 <meta property="og:description" content="在中国的传统文化中，尊重和关心是相互关联的，而表达尊重和关心的方式也有很多种。其次，给领导点奶茶也是一种职场礼仪。在单位里，给领导点奶茶可以视为一种职场礼仪，表示自己对领导的尊重和关心，同时也是一种表示礼貌和…">
 <meta property="og:title" content="职场下午茶，如何把握？_领导_奶茶_方式">
 <meta charset="utf-8">
 <meta name="data-spm" content="smpc">
 <meta name="renderer" content="webkit">
 <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
 <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
 <link rel="dns-prefetch" href="//statics.itc.cn">
 <link rel="dns-prefetch" href="//g1.itc.cn">
 <link rel="dns-prefetch" href="//js.sohu.com">
 <link rel="icon" href="//statics.itc.cn/web/static/images/pic/sohu-logo/favicon.ico" type="image/x-icon">
 <link rel="shortcut icon" href="//statics.itc.cn/web/static/images/pic/sohu-logo/favicon.ico" type="image/x-icon">
 <link rel="apple-touch-icon" sizes="57x57" href="//statics.itc.cn/web/static/images/pic/sohu-logo/logo-57.png">
 <link rel="apple-touch-icon" sizes="72x72" href="//statics.itc.cn/web/static/images/pic/sohu-logo/logo-72.png">
 <link rel="apple-touch-icon" sizes="114x114" href="//statics.itc.cn/web/static/images/pic/sohu-logo/logo-114.png">
 <link rel="apple-touch-icon" sizes="144x144" href="//statics.itc.cn/web/static/images/pic/sohu-logo/logo-144.png">
 <link rel="preload" href="https://g1.itc.cn/msfe-pcarti-prod/300000000000/assets/css/main_article-d50fe5.css" as="style">
 <link href="https://g1.itc.cn/msfe-pcarti-prod/300000000000/assets/css/main_article-d50fe5.css" rel="stylesheet">
 </head>
 <body class="article-page" data-region="157" data-spm="content" data-newsid="749607511">
 <div class="wrapper-box">
  <header id="main-header" class="error-head">
  <div class="head-container">
   <div class="head-nav" data-spm="nav">
   <ul>
    <li class="index"><a data-clev="10220248" class="clearfix" target="_blank" href="http://www.sohu.com"> <span class="sohu-logo"></span> </a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220249" href="http://news.sohu.com/">新闻</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220250" href="http://sports.sohu.com/">体育</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220251" href="http://auto.sohu.com/">汽车</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220252" href="http://www.focus.cn/">房产</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220253" href="http://travel.sohu.com/">旅游</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220254" href="http://learning.sohu.com/">教育</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220255" href="http://fashion.sohu.com/">时尚</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220256" href="http://it.sohu.com/">科技</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220257" href="http://business.sohu.com/">财经</a></li>
    <li class="nav-item"><a target="_blank" data-clev="10220258" href="http://yule.sohu.com/">娱乐</a></li>
    <li class="nav-item more-nav">
    <div class="more-tag" href="javascript:void(0)"><span>更多</span>
     <div class="cor"></div>
    </div><more-nav id="moreNav"></more-nav></li>
   </ul>
   </div><head-right id="headRight"></head-right>
  </div>
  </header>
  <div class="location-without-nav"></div>
  <div class="area clearfix" id="article-container">
  <div class="column left" style="min-height: 200px">
   <div class="user-info" id="user-info" data-spm="author">
   <div class="user-pic"><!-- fromWhere为10是马甲号作者不可点击进入个人页面 --> <a href="https://mp.sohu.com/profile?xpt=ZWZlZjBmM2ItMGY4MC00MDE3LWEwNWEtYTkxZjg0MTlkYmFi" target="_blank"> <img data-src="//p9.itc.cn/q_70/images03/20231106/27bbcb76999b4d1488640606ab8089f0.jpeg" alt=""> </a>
   </div>
   <h4><a href="https://mp.sohu.com/profile?xpt=ZWZlZjBmM2ItMGY4MC00MDE3LWEwNWEtYTkxZjg0MTlkYmFi" target="_blank">骑着小木马走天下</a></h4><!-- 积分 -->
   <dl class="user-num">
    <dd>
    <span class="value" data-value="131" data-role="info-article-num"><em class="num"></em></span>文章
    </dd>
    <dd>
    <span class="value" data-value="" data-role="info-read-num"><em class="num"></em></span>总阅读
    </dd>
   </dl><!-- 企业认证 -->
   <ul class="company">
   </ul><!-- 非马甲号作者 -->
   <div class="user-more"><a href="https://mp.sohu.com/profile?xpt=ZWZlZjBmM2ItMGY4MC00MDE3LWEwNWEtYTkxZjg0MTlkYmFi" target="_blank">查看TA的文章&gt;</a>
   </div>
   </div><!-- 互动&分享 -->
   <div class="share-interaction" id="shareInteraction"><share-interaction />
   </div>
  </div>
  <div class="left main">
   <div data-spm="content">
   <div class="text">
    <div class="text-title">
    <h1>职场下午茶，如何把握？ <span class="article-tag"> </span></h1>
    <div class="article-info"><span class="time" id="news-time" data-val="1704379583000"> 2024-01-04 22:46 </span>
     <div class="area">
     <span>发布于：</span><span>湖南省</span>
     </div>
    </div>
    </div>
    <article class="article" id="mp-editor"><!-- 政务处理 -->
    <p>身为一个员工，在单位里给领导点奶茶是一种常见的礼仪，也是一种表示尊重和关心的方式。不过，这并不意味着这种行为是必须的或者被要求的，而是出于个人的意愿和考虑。</p>
    <p class="ql-align-center"><img max-width="600" data-src="vrQqgk+FQSQmr7dDCa0gdmxFpXQMjE072vLATABxk7BLR3WCibGeje7VWY0RednwovzVERkkNkxlHZI8vVd5ebWTzmKYPwYvFkmu9a+AK6w="></p>
    <p class="ql-align-center"><img max-width="600" data-src="j62ER+laWpTPEkLaFdmRXpIrV60ddatV8GWqID84jSiwii90fF7tAsXWQZ6s4ULy0ZdaPYicNXQYbZD0UKvuULWTzmKYPwYvFkmu9a+AK6w="></p>
    <p class="ql-align-center"><img max-width="600" data-src="CZMT6o4i3vOAFZsV462x35a+eiGEPFU8kEKKQFFid5ogZhuxp28jP3FHU6fqmoGa4yPYhozpgFN2kK+HF/bJprWTzmKYPwYvFkmu9a+AK6w="></p>
    <p>首先，给领导点奶茶是一种表达尊重和关心的方式。在中国的传统文化中，尊重和关心是相互关联的，而表达尊重和关心的方式也有很多种。在单位里，给领导点奶茶可以视为一种表示尊重和关心的方式，同时也是一种拉近与领导之间关系的方式。通过这种行为，可以向领导展示自己的细心和体贴，增加自己在领导心目中的好感度。其次，给领导点奶茶也是一种职场礼仪。在职场中，礼仪是非常重要的，因为它关系到个人形象和人际关系。在单位里，给领导点奶茶可以视为一种职场礼仪，表示自己对领导的尊重和关心，同时也是一种表示礼貌和友好的方式。这种礼仪可以促进职场中的人际关系，增强团队的凝聚力和合作精神。当然，给领导点奶茶也要适度。如果过度或者频繁地给领导点奶茶，可能会让领导感到不舒服或者产生负担。同时，也要注意选择合适的奶茶品牌和口味，避免因为选择不当而产生不必要的误会或者尴尬。总之，在单位里给领导点奶茶是一种常见的礼仪和表示尊重和关心的方式，但要适度、适当、适宜。只有在合适的时机和场合下，才能充分发挥其作用，促进职场中的人际关系和合作精神。<a href="//www.sohu.com/?strategyid=00001 " target="_blank" title="点击进入搜狐首页" id="backsohucom" style="white-space: nowrap;"><span class="backword"><i class="backsohu"></i>返回搜狐，查看更多</span></a></p>
    </article>
    <div id="articleTransfer">
    <transfer />
    </div><!-- 评论禁言通知 -->
    <div id="bannedNotice">
    <banned-notice />
    </div>
    <div class="statement">
    平台声明：该文观点仅代表作者本人，搜狐号系信息发布平台，搜狐仅提供信息存储空间服务。
    </div>
    <div class="bottom-relate-wrap clear type-3">
    <div id="article-like" data-like-type="type-3"><article-like />
    </div>
    <div class="read-wrap"><span class="read-num">阅读 (<em data-role="pv" data-val="$articleStat.pv"></em>)</span>
    </div>
    <div id="articleReport"><report />
    </div>
    </div>
    <div id="sohu-play-content"></div>
   </div>
   </div>
   <div data-spm="middle-banner-ad">
   </div>
   <div id="articleAllsee" style="height:629px">
   <all-see-list />
   </div>
   <div class="_0u4o3bh76zbp"></div>
   <div class="god-article-bottom" id="god_bottom_banner" data-spm="ad-text-bottom" style="display:block">
   </div>
   <div class="user-god clear" id="user-post" style="display:none">
   </div><!-- 评论 -->
   <div id="meComment" style="min-height: 100px;"><me-comment />
   </div>
   <div id="commentList"><comment-list></comment-list>
   </div>
   <div id="discuss"></div><!-- 推荐阅读 -->
   <div style="min-height:1500px" id="groomRead"><groom-read />
   </div>
  </div><!-- 右侧边栏 -->
  <div class="sidebar right" id="right-side-bar" data-a="${isBaiDuAd}"><right-side-bar />
  </div>
  </div>
  <div id="float-btn"><float-btn />
  </div>
  <div class="left-bottom-float-fullScreenSleepContainer" style="display:none;">
  <div class="left-bottom-float-fullScreenSleep" style="display:none;" data-spm="ad-fullScreenSleep">
   <div class="close-tag"></div>
  </div>
  </div>
  <div class="left-bottom-float" id="left-bottom-god" data-spm="ad-ss">
  </div>
 </div>
 <script type="text/javascript">
            window.deployEnv = "prod"
          </script>
 <script src="//js.sohu.com/pv.js"></script>
 <script src="https://g1.itc.cn/msfe-pcarti-prod/300000000000/assets/js/vendors-9739fe.js"></script>
 <script src="https://g1.itc.cn/msfe-pcarti-prod/300000000000/assets/js/c.main_article.main_article_moment.main_focus.main.main_focus_video.main_focus_pictures.main_na.main_focus_home-2979ff.js"></script>
 <script src="https://g1.itc.cn/msfe-pcarti-prod/300000000000/assets/js/main_article-58946f.js"></script>
 <script>
try {
    var cfgs = {
    channel_id: "31",
    news_id: "749607511",
    cms_id: "$mpNews.cmsId",
    media_id: "121846184",
    passport: "1721406086294081536@sohu.com",
    weboUrl: "https://mp.sohu.com/profile?xpt=ZWZlZjBmM2ItMGY4MC00MDE3LWEwNWEtYTkxZjg0MTlkYmFi",
    title: "职场下午茶，如何把握？",
    channel_url: "/c/31",
    integralLevel: "0",
    categoryId: "-1",
    //abData_fd用于abtest
    abData: "",
    // abData_discuss:"4", // 讨论
    abData_discuss: "", // 讨论
    abData_fd: "",
    abData_tw: "",
    originalId: "$mpNews.originalId",
    originalStatus: "0",
    isBaiDuAd: "",
    isPure: "${pure}",
    reprint: false,
    reprintSign: "",
    secureScore: '100',
    sGrade: '0',
    hideAd: '',
    hiddenRatio: '0',
    keywords: "[礼仪, 职场, 关系, 单位, 领导, 是一种, 个人, 方式, 奶茶, 行为, 礼仪, 人际, 职场, 领导, 奶茶]",
    mpNewsExt: {
      "modelId": ""
    },
    imgsList: [
                   {
        "url": "//q8.itc.cn/images01/20240104/34f76961bdb04011b8c0506e8241bab4.jpeg",
        "width": "1166",
        "height": "1545",
      }
                  , {
        "url": "//q3.itc.cn/images01/20240104/2824647a06b54cb1a3e48526f82f8f41.jpeg",
        "width": "1170",
        "height": "1539",
      }
                  , {
        "url": "//q4.itc.cn/images01/20240104/8d46b4af8f714c66a7ac077f036af0c2.jpeg",
        "width": "1170",
        "height": "1162",
      }
                ],
    topNavigation: [
                   {
        "url": "http://news.sohu.com/",
        "name": "新闻",
      }
                  , {
        "url": "http://sports.sohu.com/",
        "name": "体育",
      }
                  , {
        "url": "http://auto.sohu.com/",
        "name": "汽车",
      }
                  , {
        "url": "http://www.focus.cn/",
        "name": "房产",
      }
                  , {
        "url": "http://travel.sohu.com/",
        "name": "旅游",
      }
                  , {
        "url": "http://learning.sohu.com/",
        "name": "教育",
      }
                  , {
        "url": "http://fashion.sohu.com/",
        "name": "时尚",
      }
                  , {
        "url": "http://it.sohu.com/",
        "name": "科技",
      }
                  , {
        "url": "http://business.sohu.com/",
        "name": "财经",
      }
                  , {
        "url": "http://yule.sohu.com/",
        "name": "娱乐",
      }
                  , {
        "url": "http://baobao.sohu.com/",
        "name": "母婴",
      }
                  , {
        "url": "https://healthnews.sohu.com/",
        "name": "健康",
      }
                  , {
        "url": "http://history.sohu.com/",
        "name": "历史",
      }
                  , {
        "url": "http://mil.sohu.com/",
        "name": "军事",
      }
                  , {
        "url": "http://chihe.sohu.com/",
        "name": "美食",
      }
                  , {
        "url": "http://cul.sohu.com/",
        "name": "文化",
      }
                  , {
        "url": "http://astro.sohu.com/",
        "name": "星座",
      }
                  , {
        "url": "https://www.sohu.com/xchannel/TURBd01EQXhPVGt5",
        "name": "专题",
      }
                  , {
        "url": "http://game.sohu.com/",
        "name": "游戏",
      }
                  , {
        "url": "http://fun.sohu.com/",
        "name": "搞笑",
      }
                  , {
        "url": "http://acg.sohu.com/",
        "name": "动漫",
      }
                  , {
        "url": "http://pets.sohu.com/",
        "name": "宠物",
      }
                ],
    // 展示模式控制（0-无限制 1-8分 2-登录 3-订阅 4-付费）
    displayMode: "0",
    // 文章类型（客户端获取剩余内容接口路径参数）
    stage: "",
    // 前插视频字段
    videoId: "",
    site: "",
    HVTitle: ""
  }
} catch (e) {
  var html = '<div class="err-js">' +
    '<span><em class="icon err-js-icon"></em>JS加载错误，请重新加载。</span>' +
    '<a href="javascript:window.location.reload()" target="_blank" class="cached-btn"' +
    '><em class="icon-cached"></em>刷新</a></div>';
  document.body.innerHTML = html;
  console.error("发生错误", e);
}
</script>
 <script>
try {
  const articleBlock = cfgs.displayMode == '1'
  if (articleBlock) {
    window.sohu_mp.contentControl(cfgs);
  } else {
    window.sohu_mp.article(cfgs);
  }
} catch (e) {
  var html = '<div class="err-js">' +
    '<span><em class="icon err-js-icon"></em>JS加载错误，请重新加载。</span>' +
    '<a href="javascript:window.location.reload()" target="_blank" class="cached-btn"' +
    '><em class="icon-cached"></em>刷新</a></div>';
  document.body.innerHTML = html;
  console.error("发生错误", e);
}
</script><!-- 文章安全分低于等于10分不执行seo优化 -->
 <script>
  (function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
      bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';    
    }
    else {
      bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
  })();
</script>
 <script type="text/javascript" src="https://cpro.baidustatic.com/cpro/ui/c.js" async defer></script><!-- 头条SEO上报JS -->
 <script>
      (function(){
        var el = document.createElement("script");
        el.src = "https://lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?2a4809d3df819205088b399807ab2dfb6008be35d3aa4b8fc28d959eee7f7b82c112ff4abe50733e0ff1e1071a0fdc024b166ea2a296840a50a5288f35e2ca42";
        el.id = "ttzz";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(el, s);
      })(window)
    </script>
 </body>
</html>"""

    def test_01_extract_meta_data(self):
        meta_data = extract_meta_data(self.html)
        print(f"meta_data is: {meta_data}")

    def test_02_extract_title(self):
        title = extract_title(self.html)
        print(f"title is: {title}")

    def test_03_extract_content(self):
        content = extract_content(self.html)
        print(f"content is: {content}")

    def test_04_extract_publish_date(self):
        publish_date = extract_publish_date(self.html)
        print(f"publish_date is: {publish_date}")

if __name__ == '__main__':
    unittest.main()
