from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView ,RetrieveUpdateAPIView
from.models import Profile
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
# this is api decomation
# http://127.0.0.1:6589/api-documentation/

from django.http import HttpResponse
import json
from django.http import JsonResponse,HttpResponseForbidden
from django.core.serializers import serialize
from accounts.models import Friend

#     show all friend request : بتشوف طلبات الصداقه ال مبعوته لك   

def friend_request_api(request,slug):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.slug == slug:
        friend_requests = profile.friend_request.all()
        friend_requests_data = serialize('json', friend_requests)
        return JsonResponse(friend_requests_data, safe=False)
    else:
        return JsonResponse("You don't have permission to view this friend request.", safe=False)
    

#        accpet firend 

def accecpt_friend_request_api(request,slug):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        profile=get_object_or_404(Profile,slug=slug)
        profile.friend.add(user_profile.friend_profile)
        user_profile.friend.add(profile.friend_profile)
        user_profile.friend_request.remove(profile.friend_profile)
        user_profile.save()
        profile.save()

# show all user can send request for him :  ارسال طلب صداقه ل اي شخص محتاجه 


def add_friend_api(request):
    add_friends = Profile.objects.all().exclude(user=request.user)
    add_friends_data = serialize('json', add_friends)
    return JsonResponse(add_friends_data, safe=False)


# send rquest for user can send request for him :  ارسال طلب صداقه ل اي شخص محتاجه 

def send_request_api(request,slug):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        profile=get_object_or_404(Profile,slug=slug)
        profile.friend_request.add(user_profile.friend_profile)
        profile.save()
        print('ture')
    return redirect('/api/add_friend/')



def search_name(request,slug):
    if slug:
        search_name_friend = Profile.objects.filter(user__username__icontains=slug)
        search_name_friend_serialize = serialize('json', search_name_friend)
    return JsonResponse(search_name_friend_serialize, safe=False)



def show_request_api(request,slug):
    user_profile = get_object_or_404(Profile, user=request.user)
    if user_profile.slug == slug:
        if request.user.is_authenticated:
            profile=get_object_or_404(Profile,slug=user_profile.slug)
            profile=user_profile.friend.all()
            myfriend_serialize = serialize('json', profile)
    else:
        return JsonResponse("You don't have permission to view  list friend for this user.", safe=False)
    
    return JsonResponse(myfriend_serialize, safe=False)
