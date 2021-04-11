from django.shortcuts import render
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
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
        name = "medico"
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0
        }
        name = "administracion"
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0
        }

    class Django:
        model = Post

        fields = [
            'id', 'indice','title', 'description','order','slug'
        ]
        

def search(request):
    q = request.GET.get('q')
    id=request.GET.get('indice')

    if id=="medico":
        pr = MultiMatch(query=q, fields=['title', 'description'], fuzziness='AUTO')
        medico= PostDocument.search().query(pr)
        #medico = PostDocument.search().query('match',title=q)
        return render(request,'search.html',{'medico': medico})

    elif id=="posts":
        pr = MultiMatch(query=q, fields=['title', 'description'], fuzziness='AUTO')
        posts= PostDocument.search().query(pr)
        #posts = PostDocument.search().query('match',title=q)
        return render(request,'search.html',{'posts': posts})

    elif id=="administracion":
        pr = MultiMatch(query=q, fields=['title', 'description'], fuzziness='AUTO')
        admin= PostDocument.search().query(pr)
        #admin = PostDocument.search().query('match',title=q)
        return render(request,'search.html',{'administracion': admin})
    
    else:
        posts=''


    return render(request,'search.html',{'posts': posts})
