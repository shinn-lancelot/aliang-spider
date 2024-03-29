import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.request import urlopen

# 喜马拉雅 - 《蜢哥的烦恼生活》
url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=51851882&sort=0&pageNum='
trackDataUrl = 'https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1'
newUrl = ''
headers={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
}
dataList = []
totalPage = 15
fileName = 'dataList1.json'
originalAudioFolder = 'audio'

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
            newUrl = url + str(p)
        response = requests.get(newUrl, headers = headers)
        jsonData = response.json()
        for v in jsonData['data']['tracks']:
            dataList.append({
                'trackId': v['trackId'],
                'title': v['title']
            })

    with open(fileName, mode = 'w', encoding = 'utf-8') as f:
        json.dump(dataList, f)

# 第二步，根据音轨ID爬取音频
folder = os.path.exists(originalAudioFolder)
if not folder:
    os.makedirs(originalAudioFolder)
for i in range(len(dataList)):
    data = dataList[i]
    response = requests.get(trackDataUrl % (data['trackId']), headers = headers)
    jsonTrackData = response.json()
    trackSrc = jsonTrackData['data']['src']
    ext = trackSrc.split('.')[-1] # 原为m4a格式
    # 此处直接存为mp3
    ext = 'mp3'
    fileName = str(i + 1) + '.' + data['title'] + '.' + ext
    response = urlopen(trackSrc)
    file = response.read()
    with open(originalAudioFolder + '/' + fileName, 'wb') as f:
        print('save -> %s ' % fileName)
        f.write(file)