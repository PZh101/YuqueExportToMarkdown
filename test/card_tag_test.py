import urllib
from urllib import parse
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# file
# s = r"data:%7B%22uid%22%3A%221616394855692-0%22%2C%22src%22%3A%22https%3A%2F%2Fwww.yuque.com%2Fattachments%2Fyuque%2F0%2F2021%2Fzip%2F10362037%2F1616394954849-6e2f222d-cf9a-4d9c-a9de-02d16bf4d331.zip%22%2C%22name%22%3A%22idea%E7%A0%B4%E8%A7%A3%E8%A1%A5%E4%B8%81.zip%22%2C%22size%22%3A3444%2C%22type%22%3A%22application%2Fzip%22%2C%22ext%22%3A%22zip%22%2C%22progress%22%3A%7B%22percent%22%3A99%7D%2C%22status%22%3A%22done%22%2C%22percent%22%3A0%2C%22id%22%3A%22kaDuh%22%7D"
# yueque
s = r"data:%7B%22mode%22%3A%22embed%22%2C%22heightMode%22%3A%22default%22%2C%22src%22%3A%22https%3A%2F%2Fwww.yuque.com%2Fyixiaobai-g9f0f%2Fgoxz1b%2Fzdyebuksaydl03mh%22%2C%22url%22%3A%22https%3A%2F%2Fwww.yuque.com%2Fyixiaobai-g9f0f%2Fgoxz1b%2Fzdyebuksaydl03mh%3Fview%3Ddoc_embed%22%2C%22detail%22%3A%7B%22image%22%3A%22https%3A%2F%2Fcdn.nlark.com%2Fyuque%2F0%2F2023%2Fpng%2F10362037%2F1694163500372-56d23185-ce74-4b1c-b662-dd033d77d048.png%22%2C%22title%22%3A%22%E8%BD%AF%E4%BB%B6%E4%B8%8B%E8%BD%BD%22%2C%22type%22%3A%22doc%22%2C%22belong%22%3A%22%E8%AE%B0%E5%BD%95%22%2C%22belong_url%22%3A%22%2Fyixiaobai-g9f0f%2Fgoxz1b%22%2C%22desc%22%3A%22solidworks%E7%A0%B4%E8%A7%A3%E7%89%88%E8%AF%B4%E6%98%8E%E7%BD%91%E5%9D%80%EF%BC%9Ahttps%3A%2F%2Fwww.jb51.net%2Fsofts%2F855951.html%23downintro2%E5%9C%B0%E5%9D%80%EF%BC%9Ahttps%3A%2F%2Fpan.baidu.com%2Fshare%2Finit%3Fsurl%3DdxmiQt1CKNWDmM5KIksAUg%E6%8F%90%E5%8F%96%E7%A0%81%EF%BC%9Aeocb%22%2C%22url%22%3A%22https%3A%2F%2Fwww.yuque.com%2Fyixiaobai-g9f0f%2Fgoxz1b%2Fzdyebuksaydl03mh%22%2C%22target_type%22%3A%22Doc%22%2C%22_serializer%22%3A%22web.editor_link_detail%22%7D%2C%22id%22%3A%22R6DaI%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%7D"
s = s[5:]
# 将\u7834 转为具体的数字
# s1.decode("unicode-escape")
jsonStr = urllib.parse.unquote(s, encoding='utf-8')
print(jsonStr)
obj = json.loads(jsonStr)
fp = sys.stdout
json.dump(obj, fp, indent=2,ensure_ascii=False)
"""
{
  "uid": "1616394855692-0",
  "src": "https://www.yuque.com/attachments/yuque/0/2021/zip/10362037/1616394954849-6e2f222d-cf9a-4d9c-a9de-02d16bf4d331.zip",
  "name": "idea破解补丁.zip",
  "size": 3444,
  "type": "application/zip",
  "ext": "zip",
  "progress": {
    "percent": 99
  },
  "status": "done",
  "percent": 0,
  "id": "kaDuh"
}
"""
