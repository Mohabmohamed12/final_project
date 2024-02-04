from django.urls import path 
from .views import *
from . import views
# from.api_view import *
app_name='chat'
from .api_view import *

urlpatterns = [
    path('',views.home,name='home'),
    path('chat/',views.main,name='main'),
    path('chat_details/<slug:slug>',views.chat_details,name='chat_details'),
    path('send_message/<slug:slug>',views.send_message,name='send_message'),
    path('receive_message/<slug:slug>',views.receive_message,name='receive_message'),
    path('friend_request/<slug:slug>',views.friend_request,name='friend_request'),
    path('add_friend/',views.add_friend,name='add_friend'),
    path('send_request/<slug:slug>',views.send_request,name='send_request'),
    path('accecpt_friend_request/<slug:slug>',views.accecpt_friend_request,name='accecpt_friend_request'),
    path('friend-list/<slug:slug>',views.show_friend_list,name='show_friend_list'),
    path('remove-friend-request/<slug:slug>',views.remove_firnd_request,name='remove_firnd_request'),
    path('remove-friend-list/<slug:slug>',views.remove_firnd_list,name='remove_firnd_list'),
    # path('search-list/',views.search_list,name='search_list'),
    # path('hotel/',PropertyList.as_view(),name='property_list'),
    # path('hotel/<slug:slug>',PropertyDetail.as_view(),name='property_detail'),
    # path('create/',PropertyCreate.as_view(),name='property_create'),
    
    
    # # api
    # path('property/list',PropertyAPiList.as_view(),name='PropertyAPiList'),
    # path('property/list/<int:pk>',PropertyAPiDetail.as_view(),name='PropertyAPiDetail'),
    
    path('api/friend_request/<slug:slug>',friend_request_api,name='friend_request_api'),
    path('api/accecpt_friend_request/<slug:slug>',accecpt_friend_request_api,name='accecpt_friend_request_api'),
    path('api/add_friend/',add_friend_api,name='add_friend_api'),
    path('api/send_request/<slug:slug>',send_request_api,name='send_request_api'),
    path('api/search_name/<slug:slug>',search_name,name='search_name'),
    path('api/my-friend-list/<slug:slug>',show_request_api,name='show_request_api'),
]
