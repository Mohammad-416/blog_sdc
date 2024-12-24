from django.contrib import admin
from .models import *

for model in [CustomUser, Blog, Comment, Like]:
    admin.site.register(model)
