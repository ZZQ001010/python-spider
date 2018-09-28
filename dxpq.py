
import requests
import  re
import json
import urllib

searchName = input()

localPath = 'D://python demo/fetchImg/img/'
index_url='https://s.taobao.com/search?q='+searchName

response=requests.get(index_url)
html =response.text
data=re.findall(r'g_page_config = (.*?)g_srp_loadCss', html, re.S)[0]
#  清洗数据，去掉首位的非法字符串， 空格，回车
data= data.strip(' ;\n')
data = json.loads(data)
#取出商品列表记录
data = data['mods']['itemlist']['data']['auctions']
#处理商品的数据
goods_info =[]
for item in data:
    temp = {
        'title': item['title'],
        'pic_url': item['pic_url'],
        'view_price': item['view_price'],
    }
    goods_info.append(temp)

#保存数据，保存excel
fb=open('result.csv','w',encoding='utf_8_sig')
#写表头
fb.write('标题,图片地址,价格\n')

#下载图片函数
def dowloadPic(imageUrl,filePath):
    r = requests.get(imageUrl)
    with open(filePath, "wb") as code:
        code.write(r.content)


count = 0
for item in goods_info:
    imgurl = 'http:'+item['pic_url']
    print(imgurl)
    path = localPath+str(count)+'.jpg'
    print(path)
    dowloadPic(imgurl,path)
    temp = '{title},{pic_url},{view_price}\n'.format(**item)
    fb.write(temp)
    count=count+1
fb.close()



