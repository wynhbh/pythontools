import mmh3
import base64
import requests

favicon_file = 'https://www.baidu.com/favicon.ico'   #
response = requests.get(favicon_file)
favicon = base64.b64encode(response.content)
hash_result = mmh3.hash(favicon)

print(hash_result)
