from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Post

def home_view(request, *args, **kwargs):
    return render(request, template_name='pages/home.html', context={}, status=200)

def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    post_list = [{'id':x.id, 'content':x.content} for x in qs]
    data = {
        'response':post_list
    }
    status=200
    return JsonResponse(data, status=status)

def post_detail_view(request, post_id, *args, **kwargs):
    '''REST API VIEW'''

    data = {
        "id":post_id,
    }

    status = 200
    try:
        post = Post.objects.get(id=post_id)
        data['content'] = post.content

    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)
