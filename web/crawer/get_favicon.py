import mmh3
import requests

favicon_file = ''
response = requests.get(favicon_file)
favicon = response.content.encode('base64')
hash_result = mmh3.hash(favicon)

print(hash)
