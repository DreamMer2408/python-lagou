import requests
import json
import pymongo

headers={
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Content-Length': '55',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'www.lagou.com',
'Origin':
    'https://www.lagou.com',
'Referer': 'https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?labelWords=&fromSearch=true&suginput=',
'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
'Cookie': 'user_trace_token=20180107174149-fbb8dca9-f38e-11e7-a01c-5254005c3644; LGUID=20180107174149-fbb8e6a2-f38e-11e7-a01c-5254005c3644; _ga=GA1.2.1807318584.1515318108; X_HTTP_TOKEN=41123bf4f6003fa0f47b65749287a016; _putrc=ACFF2E8E1056FCDE; JSESSIONID=ABAAABAAAIAACBI9091AC3B38AD9F4BBFC751068DB89BA3; login=true; unick=%E7%8E%8B%E8%83%9C%E5%8D%9A; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; index_location_city=%E5%85%A8%E5%9B%BD; WEBTJ-ID=20180320221620-16243c4999b3f4-0bf73c6c19bcd2-3f3c5b02-1049088-16243c4999c21d; witkey_login_authToken="ZdsK1gjSdK+6TPdBftgs5v3tUbJXu4PkMM4Mzq6R3bSpgUbmH1OLoNY8p5GLJQNdpJ3m/7Lkd6GGRvX3qidktum9fF6V/cUVP+zdyVzqa/P1jLZubWkxUJnoJDRVmSDCg0sUbTooHlPzCVf0rFcuEVDFXzHQy9x9ow3rPbF04b94rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; hasDeliver=87; _gid=GA1.2.851477747.1523025272; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522634435,1522653689,1522824738,1523074293; gate_login_token=72fcd6f8c930008f494568262aebc0378e3906027e83f1cb; TG-TRACK-CODE=index_search; LGSID=20180407130628-6deb1612-3a21-11e8-b5f0-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%259C%25BA%25E5%2599%25A8%25E5%25AD%25A6%25E4%25B9%25A0%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20180407130628-6deb17ca-3a21-11e8-b5f0-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523077585; SEARCH_ID=5622394df38641a286f5a90d43995052'
}

client=pymongo.MongoClient('localhost',27017)
job=client['job']
table=job['jobs']
def getRequests(url,page):
    data={
        'first': 'true',
        'pn': page,
        'kd': '机器学习'
    }
    response=requests.post(url,headers=headers,data=data)
    print(page)
    getInfo(response.text)

def getInfo(response):
    reJson=json.loads(response)
    try:
        reDict=reJson['content']['positionResult']['result']
    except:
        print(reJson)
    for job in reDict:
        jobs={
            '公司':job['companyShortName'],
            '城市':job['city'],
            '位置':job['district'],
            '工作':job['positionAdvantage'],
            '学位':job['education'],
            '经验':job['workYear'],
            '标签':job['positionLables'],
            '工资':job['salary'],
        }
        save_toMongo(jobs)

def save_toMongo(jobs):
    if table.insert_one(jobs):
        print(jobs['公司']+'存入数据库')
    else:
        print(jobs['公司']+'存数据失败')
if __name__ == '__main__':
    for i in range(1,31):
        getRequests('https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false',page=i)
