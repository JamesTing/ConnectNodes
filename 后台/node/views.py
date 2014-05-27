#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.utils import simplejson
from node.models import urlToHtml,productKeyword
import bottlenose
import urllib2
#载入结巴分词
import jieba
import jieba.posseg as pseg
#载入淘宝接口
#import top.api
from xml.etree.ElementTree import fromstring

def index(request):
    return render_to_response('node/default.html')

def script(request, unionName, unionId, block):
    code = '''
    document.write("<script type='text/javascript' src='http://connectnodes.com/static/jquery.poshytip.min.js'></script>");	
	
    var poshycss = document.createElement('link');
    poshycss.rel = 'stylesheet';
    poshycss.type = 'text/css';
    poshycss.href = 'http://connectnodes.com/static/poshytip.css';
    document.getElementsByTagName('head')[0].appendChild(poshycss);
	
    jQuery(document).ready(function(){
      $.ajax({
        type: "get",
        async: false,
        url: "http://connectnodes.com/gethtml/" + encodeURIComponent(window.location.href) + "/",
        dataType: "jsonp",
        timeout: '10000',
        jsonp: "callback",
        jsonpCallback:"callback",
        success: function(json){
          if (json.output == 0) {
            var codes = encodeURIComponent($('.%s').html());
            var url = "http://connectnodes.com/switch/" + codes + "/url/" + encodeURIComponent(window.location.href) + "/";
            var script = document.createElement('script');
            script.setAttribute('src', url);
            document.getElementsByTagName('head')[0].appendChild(script);
          } else{
            $('.%s').html(decodeURIComponent(json.output));
          };  
        }
      });


      //Add Poshytip
      $('.%s dfn').poshytip({
        className: 'simple',
        liveEvents: true,
		fade: true,
		offsetY: 20,
        content: function(updateCallback) {
          var rel = $(this).attr('rel');
          return "<iframe src='http://connectnodes.com/%s/%s/" + rel + "/' width='349' height='166' border='0' frameborder='0' scrolling='no' marginwidth='0' allowtransparency='true' marginheight='0'></iframe>";
        }
      });
    });''' 
    code = code.decode('utf-8') % (block, block, block, unionName, unionId)
    return HttpResponse(code, mimetype='application/javascript;')

def gethtml(request,path):
    result = urlToHtml.objects.filter(url = path)
    if result:
        data = "callback({'output':%s})" % repr(result[0].htmlstring).lstrip('u')
        #debug()
    else:
        data = "callback({'output':0})"
    return HttpResponse(data, mimetype='application/javascript;')

def convert(string):
    seg_list = pseg.cut(string)
    #解析文本中的名词
    html = []
    productTxt = open("/engine/link/dict/productkeyword.txt")
    productWord = []
    for line in productTxt:
        productWord.append(line.rstrip('\r\n'))
    #debug()
    #将分词后的字典遍历
    for value in seg_list:
        #如果该元素是名词
        if value.flag in ["nz","nr","n"]:
            #将该元素和商品关键词库每一行进行比对  
            for line in productWord:
                global find
                #如果该元素是商品关键词，加上商品链接
                if value.word.encode('utf-8') == line:
                    #标记该元素是商品关键词，跳出商品关键词库的循环
                    find = True
                    break
                else:
                    find = False
            #debug()                 
            #如果该元素不是商品关键词，直接插入html列表
            if find == True:
                html.append("<dfn style='color:#f40;font-style:normal;border-bottom:1px dashed #f40;cursor:pointer' rel='%s'>" % value.word + value.word + "</dfn>")
            else:
                html.append(value.word)
        #如果该元素不是名词，直接插入html列表
        else:
            html.append(value.word)
    productTxt.close()
    return ''.join(html)

def switch(request,string,path):
    try:
        result = urlToHtml.objects.get(url = path)
        return HttpResponse('var x="已经在碗里了。";', mimetype='application/javascript;')
    except Exception, e:
        code = convert(string)
        result = urlToHtml(url=path, htmlstring=code)
        result.save()
        return HttpResponse('var x="顺利放进碗里。";', mimetype='application/javascript;')

def importKeyword(request,txt):
    txt = open('/home/'+ txt +'.txt', 'r')
    for line in txt:
        findword =  productKeyword.objects.filter(keyword = line.rstrip('\r\n'))
        if findword:
            continue
        else:
            result = productKeyword(keyword = line.rstrip('\r\n'))
            result.save()
    txt.close()
    return HttpResponse("关键词已经存到数据库中。")

def exportKeyword(request,txt):
    document = open('/engine/link/dict/'+ txt +'.txt', 'w')
    document.truncate()
    for value in productKeyword.objects.all():
        document.write(value.keyword.encode('utf-8'))
        document.write("\n") 
    document.close()
    return HttpResponse("File has saved " + '/engine/link/dict/' + txt + '.txt')

@cache_page(60*60*24*30)
def amazon(request,unionId,keyword):
    AMAZON_ACCESS_KEY_ID = 'AKIAJORTHN3IBPMZEYYQ'
    AMAZON_SECRET_KEY = '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'
    AMAZON_ASSOC_TAG = unionId

    NS = '{http://webservices.amazon.com/AWSECommerceService/2011-08-01}'
    amazon = bottlenose.Amazon(AMAZON_ACCESS_KEY_ID, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, Region='CN')
    response = amazon.ItemSearch(Keywords= keyword, SearchIndex="All", ResponseGroup="Medium")

    root = fromstring(response)
    Items = root.findall('.//%sItem' % NS)
    goods = []

    for item in Items[1:4]:
        value = {}
        value['title'] = item.findtext('%sItemAttributes/%sTitle' % (NS,NS))
        value['image'] = item.findtext('%sMediumImage/%sURL' % (NS,NS))
        value['price'] = item.findtext('%sOfferSummary/%sLowestNewPrice/%sFormattedPrice' % (NS,NS,NS))
        value['saleslink'] = item.findtext(('%sDetailPageURL' % NS))
        goods.append(value)
    #debug()
    meta = {'keyword':keyword,'unionid':unionId,'union':'亚马逊','icon':'/static/images/amazon.png'}
    return render_to_response('node/goods.html',{'goods':goods,'meta':meta})

def taobao(request,unionId,keyword):
    keyword = urllib2.quote(keyword.encode('utf-8'))
    sandbox = True
    if sandbox:
        url = 'gw.api.tbsandbox.com'
        port = 80
        appkey = '1021386158'
        secret = "sandboxdbb58cbf2dddabdeb68698b2a"
    else:
        url = 'gw.api.taobao.com'
        port = 80
        appkey = "21531627"
        secret = "e6204d8ee36a3031f14c08d9d23ff226"	

    req=top.api.TaobaokeItemsGetRequest(url,port)
    req.set_app_info(top.appinfo(appkey,secret))

    req.fields="num_iid,title,nick,pic_url,price,click_url,commission,commission_rate,commission_num,commission_volume,shop_click_url,seller_credit_score,item_location,volume"
    req.keyword=keyword
    #默认按照信用排序
    req.sort = 'credit_desc'
    #try:
    resp = req.getResponse()['taobaoke_items_get_response']['taobaoke_items']['taobaoke_item']
        #print resp
    #except Exception, e:
        #print(e)
    #    resp = "none"

    #获取商品id名称、图片、价格、佣金、佣金比例、商家地址、商品链接
    #num_iid, title, pic_url, price, commission, commission_rate, item_location, click_url
    return render_to_response('base/goods.html',
                              {'itemlist':resp})


