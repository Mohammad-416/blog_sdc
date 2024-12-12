
import requests

url = 'https://sdcblogproject.onrender.com/api/blogs/'
headers = {
    #'Content-Type' : 'application/json',
    'Authorization': 'Bearer ' + dict["access"]
}
data = {
    'title': 'Testing Images',
    'content': 'This is a blog',
    'author_id': dict["author_id"]
}
files = {
    'images': open('C:\\users\\user\\downloads\\color.png', 'rb')
}

response = requests.post(url, headers = headers, data=data, files=files)
print(response.json())