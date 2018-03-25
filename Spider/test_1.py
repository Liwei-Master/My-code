import requests

payload = {'key1': 's', 'key2': 'x'}
r = requests.get("http://httpbin.org/get", params=payload)

print(r.text)

pay = {'key1': 's', 'key2': 'x'}
r = requests.post("http://httpbin.org/post", data=pay)

print(r.text)

