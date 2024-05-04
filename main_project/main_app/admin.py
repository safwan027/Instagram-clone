from django.contrib import admin
from  .models import (User, Post, comment, follow,profile,story)

# Register your models here.

admin.site.register(profile)
admin.site.register(comment)
admin.site.register(Post)
admin.site.register(follow)
admin.site.register(story)
