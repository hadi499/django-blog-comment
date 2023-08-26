from django.contrib import admin
from .models import BlogPost, Comment

# Register your models

admin.site.register(BlogPost)
admin.site.register(Comment)
