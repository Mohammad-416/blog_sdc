dict  = {
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzI5NTI2LCJpYXQiOjE3MzM3MjkyMjYsImp0aSI6IjE0YzhkZDg4ZWI4YjQwOTk5YTI5MGVlZDJhNGVjN2M0IiwidXNlcl9pZCI6MX0.D0A8pqdwuHTxIpvfY8smOgmUW0ylbmg1OkHz5eRVG0M",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzgxNTYyNiwiaWF0IjoxNzMzNzI5MjI2LCJqdGkiOiIwMmQ3ZjExZjY2Nzk0ZDI0ODdkYzZiNDdjNDk1ODc3YSIsInVzZXJfaWQiOjF9.EVZ0bvBfdpUAU9JINSuHFA0kFja7e7ISsVoosjKWmTM",
  "author_id": "92d38323-6c27-431a-82ca-49ffc2ecbecb"
}
import requests

url = 'http://127.0.0.1:8000/api/blogs/'
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