from django.contrib import admin
from .models import *

for model in [CustomUser, Blog, Comment]:
    admin.site.register(model)
