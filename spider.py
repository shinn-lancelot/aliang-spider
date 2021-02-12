import requests
from bs4 import BeautifulSoup
import json
import os

# 喜马拉雅 - 《阿亮的烦恼生活》
url = 'https://www.ximalaya.com/guangbojv/16804202/'
trackDataUrl = 'https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1'
newUrl = ''
headers={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
}
dataList = []
totalPage = 79
fileName = 'dataList.json'
originalAudioFolder = 'm4a'

# 第一步，爬取音轨ID及标题
if os.access(fileName, os.F_OK):
    fp = open(fileName, encoding = 'utf-8')
    dataList = json.load(fp)
    fp.close()

if len(dataList) == 0:
    for i in range(totalPage):
        p = i + 1
        newUrl = url
        if i > 0:
            newUrl = url + 'p' + str(p)
        response = requests.get(newUrl, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        divNodes = soup.find_all('div', class_ = "text lF_")
        # aNodes = soup.select('a[href^="/guangbojv/16804202/"]')
        for divNode in divNodes:
            aNodes = divNode.find_all('a')
            for a in aNodes:
                dataList.append({
                    'trackId': a['href'].split('/')[-1],
                    'title': a['title']
                })

    with open(fileName, mode = 'w', encoding = 'utf-8') as f:
        json.dump(dataList, f)

# 第二步，根据音轨ID爬取音频
folder = os.path.exists(originalAudioFolder)
if not folder:
    os.makedirs(originalAudioFolder)
for data in dataList:
    response = requests.get(trackDataUrl % (data['trackId']), headers = headers)
    jsonTrackData = response.json()
    trackSrc = jsonTrackData['data']['src']
    ext = trackSrc.split('.')[-1]
    fileName = data['title'] + '.' + ext
    res = requests.get(trackSrc, stream = True)
    filePath = os.path.join(originalAudioFolder, fileName)
    print('开始写入文件：', filePath)
    with open(filePath, 'wb') as fd:
        for chunk in res.iter_content():
            fd.write(chunk)
    print(fileName + ' 成功下载！')