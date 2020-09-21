import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import PostCreationForm
from .models import Post

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    '''HOME PAGE VIEW'''
    return render(request, template_name='pages/home.html', context={}, status=200)

def create_post_view(request, *args, **kwargs):
    form = PostCreationForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None:
            return redirect(next_url)
        form = PostCreationForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})

def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    post_list = [x.serialize() for x in qs]
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
