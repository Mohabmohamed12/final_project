from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from accounts.models import Profile,Friend
# Create your views here.
from django.shortcuts import get_object_or_404
from.models import ChatMessage
from django.db.models import Q
from itertools import chain
from django.urls import reverse
import json

def home(request):
    if request.user.is_authenticated:
        return redirect('/chat')
    return render(request,'chat/index.html',)

def main(request):
    profile = get_object_or_404(Profile, user=request.user)
    friends = profile.friend.all()
    search_name_friend = ''
    if 'searchname' in request.GET:
        slug = request.GET['searchname']
        if slug:
            search_name_friend = Profile.objects.filter(user__username__icontains=slug)
            context ={'search_name_friend' : search_name_friend}
            return render(request, 'chat/search_friends.html',context)
    return render(request,'chat/chat.html',{'profile': profile, 'friends': friends})

def chat_details(request,slug):
    profile=get_object_or_404(Profile,slug=slug)
    user_profile = get_object_or_404(Profile, user=request.user)
    msg_sender = ChatMessage.objects.filter(
        (Q(msg_sender=profile) & Q(msg_receiver=user_profile))
    ).order_by('send_in')
    msg_receiver = ChatMessage.objects.filter(
        (Q(msg_sender=user_profile) & Q(msg_receiver=profile))
    ).order_by('send_in')
    all_messages = sorted(chain(msg_sender, msg_receiver), key=lambda x: x.send_in)
    if request.method == 'POST' and 'send' in request.POST:
        chat_body = request.POST['chat_body']
        chat_text=ChatMessage.objects.create(
                                        msg_sender=user_profile,
                                        body=chat_body,
                                        msg_receiver=profile,
                                            )
        chat_text.save()
        return redirect(reverse('chat:chat_details', kwargs={'slug': profile.slug}))



    return render(request,'chat/chat_details.html',{'profile': profile,'user_profile': user_profile,'all_messages': all_messages})

def send_message(request,slug):
    profile=get_object_or_404(Profile,slug=slug)
    user_profile = get_object_or_404(Profile, user=request.user)
    data=json.loads(request.body)
    chat_body = data["msg"]
    chat_text=ChatMessage.objects.create(
                                        msg_sender=user_profile,
                                        body=chat_body,
                                        msg_receiver=profile,
                                            )
    chat_text.save()
    response_data = {
        'msg': chat_body,
        'send_in': chat_text.send_in,  # Assuming you have a 'timestamp' field in ChatMessage
        'avatar_url': user_profile.image.url if user_profile.image else '',  # Update accordingly
    }

    return JsonResponse(response_data, safe=False)
from django.core.serializers import serialize
def receive_message(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user_profile = get_object_or_404(Profile, user=request.user)
    
    # arr =[]
    # Filter messages where the sender is the other user and the receiver is the current user
    msg_receiver = ChatMessage.objects.filter(
        Q(msg_sender=profile) & Q(msg_receiver=user_profile)
    ).order_by('send_in')
    serialized_messages = serialize('json', msg_receiver, fields=('send_in', 'body', 'msg_sender__image'))

    # Deserialize the data to manipulate the structure
    data = json.loads(serialized_messages)
    arr = []

    for entry in data:
        fields = entry['fields']
        send_in = fields.get('send_in', '')  # Get the timestamp or an empty string if not present

        # Build a dictionary with the desired structure
        message_data = {
            'body': fields.get('body', ''),
            'send_in': send_in,
            'avatar_url': profile.image.url if profile.image else '', 
        }

        arr.append(message_data)

    return JsonResponse(arr, safe=False)


def friend_request(request,slug):
    profile = get_object_or_404(Profile, user=request.user)
    friend_requests = profile.friend_request.all()
    return render(request,'chat/friend_request_list.html',{'friend_requests': friend_requests})


def add_friend(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    friend=user_profile.friend.all()
    add_friends = Friend.objects.all().exclude(profile=request.user.profile)
    return render(request,'chat/add_friend.html',{'add_friends': add_friends})

def send_request(request,slug):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        profile=get_object_or_404(Profile,slug=slug)
        profile.friend_request.add(user_profile.friend_profile)
        profile.save()
    return redirect('/add_friend/')


def accecpt_friend_request(request,slug):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        profile=get_object_or_404(Profile,slug=slug)
        profile.friend.add(user_profile.friend_profile)
        user_profile.friend.add(profile.friend_profile)
        user_profile.friend_request.remove(profile.friend_profile)
        user_profile.save()
        profile.save()
    return redirect('/')


def show_friend_list(request,slug):
    user_profile = get_object_or_404(Profile, user=request.user)
    if user_profile.slug == slug:
        profile=get_object_or_404(Profile,slug=slug)
        all_friends=profile.friend.all().exclude(profile=request.user.profile)
        return render(request,'chat/all_friends.html',{'all_friends': all_friends})
    else:
        return JsonResponse("You don't have permission to view  list friend for this user.", safe=False)
    
    
    
def remove_firnd_request(request,slug):
    user_profile = get_object_or_404(Profile, slug=slug)
    login_profile = get_object_or_404(Profile, user=request.user)
    login_profile.friend_request.remove(user_profile.friend_profile)
    login_profile.save()
    return redirect('/')

def remove_firnd_list(request,slug):
    user_profile = get_object_or_404(Profile, slug=slug)
    login_profile = get_object_or_404(Profile, user=request.user)
    login_profile.friend.remove(user_profile.friend_profile)
    login_profile.save()
    return redirect('/')

# def search_list(request):
#     slug = request.GET['search']
#     if slug:
#         search_name_friend = Profile.objects.filter(user__username__icontains=slug)
#     context ={'search_name_friend' : search_name_friend}
#     return render(request, 'chat/search_friends.html',context)


# def product_list(request):
#     product_list=Product.objects.all()
#     paginator = Paginator(product_list, 6) # Show 25 contacts per page.
#     page_number = request.GET.get('page')
#     product_list = paginator.get_page(page_number)
#     name = ''
#     if 'searchname' in request.GET:
#         product_list1=Product.objects.all()
#         name = request.GET['searchname']
#         if name:
#             product_list = product_list1.filter(PRDname__icontains=name)
#     context ={'product_list' : product_list}
#     return render(request, 'product/product_list.html',context)