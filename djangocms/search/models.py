from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField
# from users.models import Role

# Create your models here.

class Post(models.Model):
    
    indice = models.CharField(max_length=255,blank=True,null=True)
    roles = models.CharField(max_length=255,blank=True,null=True)
    titulo = models.CharField(max_length=255,blank=True,null=True)
    descripcion = models.TextField(blank=True,null=True)
    metadata = models.TextField(blank=True,null=True)
    contenido = models.TextField(blank=True,null=True)
    url = models.CharField(max_length=255,blank=True,null=True)
    order = models.IntegerField(blank=True,null=True)
    slug = models.SlugField(default='',blank=True)

    def save(self):
        self.slug = slugify(self.titulo)
        super(Post, self).save()

    def str(self):
        return '%s' % self.titulo
