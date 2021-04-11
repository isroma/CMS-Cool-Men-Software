from django.db import models
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    
    indice=models.CharField(max_length=255,blank=True,null=True)
    title=models.CharField(max_length=255,blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    order=models.IntegerField(blank=True,null=True)
    slug=models.SlugField(default='',blank=True)

    def save(self):
        self.slug=slugify(self.title)
        super(Post,self).save()

    def str(self):
        return '%s' % self.title
