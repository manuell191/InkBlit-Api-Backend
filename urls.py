from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('login', views.login),
    path('user', views.users),
    path('user/<pk>/protected', views.userProtected),
    path('user/<pk>', views.user),
    path('follow', views.follows),
    path('follow/<pk>', views.follow),
    path('follows/<pk>', views.userFollows),
    path('follows/<pk>/list', views.userFollowsList),
    path('following/<pk>', views.followingUser),
    path('following/<pk>/list', views.followingUserList),
    path('following/<pk>/posts', views.followingUserPosts),
    path('following/<pk>/account/<pk2>', views.followingUserAccount),
    path('post', views.posts),
    path('post/user/<pk>', views.userPosts),
    path('post/room/<pk>', views.roomPost),
    path('post/<pk>', views.post),
    path('room', views.rooms),
    path('room/member', views.memberRooms),
    path('room/<pk>', views.room),
    path('room/admin/<pk>', views.adminRooms),
    path('room/code/<pk>', views.codeRoom),
    path('room/member/user/<pk>', views.userRooms),
    path('room/member/<pk>', views.memberRoom),
    path('room/member/<pk>/user/<pk2>', views.memberRoomUser),
    path('room/<pk>/users', views.roomUsers),
    path('room/members/<pk>', views.roomMembers),
    path('room/included/<pk>', views.roomIncluded),
    path('room/<pk>/posts', views.roomPosts)
]
