import requests

url = "http://127.0.0.1:5000/api/classify_outfit"

files = {
    'image': open('my_outfit.jpg', 'rb')
}

response = requests.post(url, files=files)
print(response.json())
