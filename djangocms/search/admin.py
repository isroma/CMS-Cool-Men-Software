from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=('indice','title','description','order','slug')

admin.site.register(Post, PostAdmin)
