import requests

BASE = "http://127.0.0.1:5000/"

data = [
  {"likes": 78, "name": "Thor", "views": 100000},
  {"likes": 10000, "name": "How to make apis", "views": 80000},
  {"likes": 150, "name": "Thor", "views": 100000}
]

for i in range(len(data)):
  #The mock response calls the method and takes the url as the paramenters
  response = requests.post(BASE + "video/" + str(i), data[i])
  print(response.json())
input()
response = requests.get(BASE + "video/2")
print(response.json())
input()
response = requests.patch(BASE + "video/2", {"likes": 99})
print(response.json())