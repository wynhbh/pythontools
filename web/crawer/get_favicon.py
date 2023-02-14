import mmh3
import requests

favicon_file = 'https://www.google.com/favicon.ico'   #
response = requests.get(favicon_file)
favicon = response.content.encode('base64')
hash_result = mmh3.hash(favicon)

print(hash_result)
