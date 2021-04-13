from django.shortcuts import render
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
from search.models import Post
from users.models import Profile

# Create your views here.

@registry.register_document
class PostDocument(Document):
    class Index:
        name = "general"
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0
        }
        name = "arquitectura"
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0
        }
        name = "django"
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0
        }

    class Django:
        model = Post

        fields = [
            'id', 'indice','titulo', 'descripcion','order','slug'
        ]
        

def search(request):
    q = request.GET.get('q')
    id = request.GET.get('indice')

    if id is None:
        return render(request,'search.html')
        
    # TODO: this only works with last name == 'django'
    elif id in PostDocument.Index.name:
        mq = MultiMatch(query=q, fields=['titulo', 'descripcion'], fuzziness='AUTO')
        posts = PostDocument.search(index=id).query(mq)

    else:
        posts = ''

    return render(request,'search.html',{'posts': posts})
