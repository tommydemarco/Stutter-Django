import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .forms import PostCreationForm
from .models import Post
from .serializers import PostSerializer, PostActionSerializer, PostCreateSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    '''home page view'''
    return render(request, template_name='pages/home.html', context={}, status=200)

@api_view(['POST']) #only allowing POST requests to this view, managed by urls.py
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    '''create post view with django rest'''
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET']) #only allowing GET requests to this view, managed by urls.py
def post_list_view(request, *args, **kwargs):
    '''list view with django rest'''
    qs = Post.objects.all()
    #print(request.is_ajax()) it is an ajax request even without xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET']) #only allowing GET requests to this view, managed by urls.py
def post_detail_view(request, post_id, *args, **kwargs):
    '''list view with django rest'''
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST']) #only allowing GET requests to this view, managed by urls.py
@permission_classes([IsAuthenticated])
def post_delete_view(request, post_id, *args, **kwargs):
    '''list view with django rest'''
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message':'You cannot delete this post'}, status=403)
    obj = qs.first()
    obj.delete()
    return Response({'message':'The post has been deleted'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Post.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "repost":
            new_post = Post.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content)
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

def create_post_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = PostCreationForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
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

def post_list_view_pure_django(request, *args, **kwargs):
    qs = Post.objects.all()
    post_list = [x.serialize() for x in qs]
    data = {
        'response':post_list
    }
    status=200
    return JsonResponse(data, status=status)

def post_detail_view_pure_django(request, post_id, *args, **kwargs):
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
