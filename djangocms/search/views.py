from django.shortcuts import render
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Post

# Create your views here.

@registry.register_document
class PostDocument(Document):
    class Index:
        name = "posts"
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0
        }

    class Django:
        model = Post

        fields = [
            'id', 'title', 'description', 'body', 'order', 'slug', 'image'
        ]
        

def search(request):
    q = request.GET.get('q')

    if q:
        posts = PostDocument.search().query('match',title=q)
    else:
        posts = ''

    return render(request,'search.html',{'posts': posts})
