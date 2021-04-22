from django.shortcuts import render
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
from search.models import Post
from users.models import Role

# Create your views here.
roles = Role.objects.all()

@registry.register_document
class PostDocument(Document):
    class Index:
        def create_indexes(self):
            for role in roles:
                name = role
                settings = {
                    'number_of_shards': 1,
                    'number_of_replicas': 0
                }

    class Django:
        model = Post

        fields = [
            'id', 'indice','titulo', 'descripcion','order','slug'
        ]
        

def search(request):
    q = request.GET.get('q')
    id = request.GET.get('indice')

    mq = MultiMatch(query=q, fields=['titulo', 'descripcion'], fuzziness='AUTO')
    posts = PostDocument.search(index=id).query(mq)

    context = {
        'posts': posts,
        'roles': roles,
        'id': id
    }

    return render(request, 'search.html', context)
