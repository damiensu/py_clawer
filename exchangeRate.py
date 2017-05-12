import json
import urllib2
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request
from google.cloud import storage
from google.cloud.storage import Blob

target_url = "http://rate.bot.com.tw/xrt?Lang=zh-TW"

data = urllib2.urlopen(target_url)
soup = BeautifulSoup(data, "html.parser")

res = {}

lastUpdate = soup.find("span", { "class" : "time" })
print lastUpdate.text

res["lastUpdate"] = str(lastUpdate.text).replace("/", "-")
res["rateData"]   = {}

for tr in soup.find_all("tr")[2:]:
    currency = tr.select(".currency .print_hide")
    #print currency
    cur = str(currency)
    curName =  cur[cur.find("(")+1:cur.find(")")]

    tds = BeautifulSoup(str(tr), "html.parser")
    curt_td = tds.find_all('td', { 'class': 'print_hide' })[1]
    curRate = str(curt_td.text)

    res["rateData"]["unit"]    = curName
    res["rateData"]["flagUrl"] = "https://storage.googleapis.com/dmnconsole/" + curName + ".png"
    res["rateData"]["rate"]    = curRate


f = open('/Users/damien/Code/dmnconsole_py/res.json', 'wt')
f.write(json.dumps(res))


client = storage.Client(project='dmn-cloud')
bucket = client.get_bucket('dmnconsole')
blob = Blob('secure-data', bucket)
with open('/Users/damien/Code/dmnconsole_py/res.json', 'rb') as my_file:
    blob.upload_from_file(my_file)
    blob.make_public()
