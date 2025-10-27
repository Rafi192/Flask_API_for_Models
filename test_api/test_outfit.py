import requests

url = "https://outfit-classification-3.onrender.com/api/classify_outfit"

with open(r"C:\Users\hasan\Rafi_SAA\python_practices\flask\Flask_API_for_Models\uploads\blazer.jpg", 'rb') as f:
    files = {'image': f}
    response = requests.post(url, files=files)

print("Status code:", response.status_code)
print("after status line----------")

try:
    print("JSON response:", response.json())
    print("after json line----------")
except:
    print("Response text:", response.text)
    print("after exception line----------")
