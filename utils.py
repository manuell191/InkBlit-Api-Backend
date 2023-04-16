'''
This file is to help clean up the looks of views.py
'''
from random import randint
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import (ProfileSerializer, UpdateProfileSerializer, FollowSerializer,
                          PostSerializer, RoomSerializer, RoomMemberSerializer)
from .models import Profile, Follow, Post, Room, RoomMember
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist

def getLogin(data):
    username = data['username']
    password = data['password']
    try:
        user = User.objects.get(username=username) #403 on error
    except ObjectDoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    success = user.check_password(password)
    if success:
        token = Token.objects.get_or_create(user=user)
        return Response({'token': token[0].key, 'user': user.username, 'id': user.id})
    return Response('Incorrect username or password', status=status.HTTP_401_UNAUTHORIZED)


def getUsers():
    profiles = Profile.objects.all().order_by('username')
    serializers = ProfileSerializer(profiles, many=True)
    return Response(serializers.data)

def createUser(data):
    user = User.objects.create_user(data['username'], data['email'], data['password'])
    user.save()
    profile = Profile.objects.create(
        user = user,
        username = data['username'],
        email = data['email'],
        bio = data['bio']
    )
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token[0].key, 'user': user.username, 'id': user.id})

def getUserProtected(pk, user):
    profile = Profile.objects.get(id=pk)
    if user != User.objects.get(id=pk):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    serializers = ProfileSerializer(profile, many=False)
    return Response(serializers.data)

def getUser(pk):
    try:
        profile = Profile.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Does not exist', status=status.HTTP_404_NOT_FOUND)
    serializers = ProfileSerializer(profile, many=False)
    return Response(serializers.data)

def updateUser(request, pk):
    user = User.objects.get(id=pk)
    if request.user != user:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    profile = get_object_or_404(Profile, id=pk)
    serializer = UpdateProfileSerializer(profile, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    if request.user != user:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    profile = Profile.objects.get(id=pk)
    profile.delete()
    user.delete()
    return Response(f'User with id {pk} was deleted')



def getFollows():
    follows = Follow.objects.all()
    serializers = FollowSerializer(follows, many=True)
    return Response(serializers.data)

def createFollow(data):
    print('here')
    account = Profile.objects.get(id=data['account'])
    following = Profile.objects.get(id=data['following'])
    follow, created = Follow.objects.get_or_create(
        account = account,
        following = following
    )
    serializers = FollowSerializer(follow, many=False)
    return Response(serializers.data)

def getFollow(pk):
    follow = Follow.objects.get(id=pk)
    serializers = FollowSerializer(follow, many=False)
    return Response(serializers.data)

def deleteFollow(request, pk):
    follow = Follow.objects.get(id=pk)
    user = User.objects.get(id=follow.account.id)
    if request.user != user:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    follow.delete()
    return Response(f'Follow with id {pk} was deleted')

def getUserFollows(pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.filter(account=user)
    serializers = FollowSerializer(follow, many=True)
    return Response(serializers.data)

def getUserFollowsList(pk):
    try:
        user = Profile.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Does not exist', status=status.HTTP_404_NOT_FOUND)
    follow = Follow.objects.filter(account=user)
    userList = Profile.objects.none()
    for i in follow:
        userList |= Profile.objects.filter(id=i.following.id)
    serializers = ProfileSerializer(userList, many=True)
    return Response(serializers.data)

def getFollowingUser(pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.filter(following=user)
    serializers = FollowSerializer(follow, many=True)
    return Response(serializers.data)

def getFollowingUserList(pk):
    try:
        user = Profile.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Does not exist', status=status.HTTP_404_NOT_FOUND)
    follow = Follow.objects.filter(following=user)
    userList = Profile.objects.none()
    for i in follow:
        userList |= Profile.objects.filter(id=i.account.id)
    serializers = ProfileSerializer(userList, many=True)
    return Response(serializers.data)

def getFollowingUserPosts(pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.filter(account=user)
    posts = Post.objects.none()
    for i in follow:
        posts |= Post.objects.filter(account=i.following, room='global')
    posts = posts.order_by('-id')
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data)

def getFollowingUserAccount(pk, pk2):
    user = Profile.objects.get(id=pk)
    follows = Follow.objects.filter(following=user)
    follow = None
    for i in follows:
        if i.account.id == int(pk2):
            print('hi')
            follow = i
    if follow == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializers = FollowSerializer(follow, many=False)
    return Response(serializers.data)

def getPosts():
    post = Post.objects.filter(room='global').order_by('-id')
    serializers = PostSerializer(post, many=True)
    return Response(serializers.data)

def createPost(data, user):
    account = Profile.objects.get(user=user)
    post = Post.objects.create(
        account = account,
        username = account.username,
        content = data['content'],
        room = 'global'
    )
    serializers = PostSerializer(post, many=False)
    return Response(serializers.data)

def getUserPosts(pk, user):
    profile = Profile.objects.get(id=pk)
    if user == profile.user:
        posts = Post.objects.filter(account=profile).order_by('-id')
    else:
        posts = Post.objects.filter(account=profile, room='global').order_by('-id')
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data)

def getPost(pk):
    post = Post.objects.get(id=pk)
    serialzers = PostSerializer(post, many=False)
    return Response(serialzers.data)

def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    user = post.account.user
    if request.user != user:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response(f'Post with id {pk} was deleted')

def createRoomPost(data, user, roomid):
    account = Profile.objects.get(user=user)
    try:
        room = Room.objects.get(id=roomid)
    except ObjectDoesNotExist:
        return Response("Does not exist", status=status.HTTP_400_BAD_REQUEST)
    rmr = RoomMember.objects.filter(room=room)
    for i in rmr:
        if i.account == account:
            print('here')
            post, created = Post.objects.get_or_create(
                account = account,
                username = account.username,
                content = data['content'],
                room = room.code
            )
            break
    try:
        serializers = PostSerializer(post, many=False)
    except UnboundLocalError:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    return Response(serializers.data)



def getRooms():
    rooms = Room.objects.all()
    serializers = RoomSerializer(rooms, many=True)
    return Response(serializers.data)

def createRoom(data, user):
    code = 0
    existing_code = True
    while existing_code:
        code = randint(111_111, 999_999)
        try:
            room = Room.objects.get(code=code)
            if room.code == code:
                existing_code = True
        except (FieldDoesNotExist, ObjectDoesNotExist) as error:
            existing_code = False
    profile = Profile.objects.get(user=user)
    room, created = Room.objects.get_or_create(
        title = data['title'],
        code = code,
        admin = profile
    )
    member = RoomMember.objects.get_or_create(
        account = profile,
        room = room
    )
    serializers = RoomSerializer(room, many=False)
    return Response(serializers.data)

def getRoom(pk):
    try:
        room = Room.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Does not exist', status=status.HTTP_404_NOT_FOUND)
    serilizers = RoomSerializer(room, many=False)
    return Response(serilizers.data)

def addById(data, pk):
    room = Room.objects.get(id=pk)
    user = Profile.objects.get(id=data['account'])
    member, created = RoomMember.objects.get_or_create(
        account = user,
        room = room
    )
    serializers = RoomMemberSerializer(member, many=False)
    return Response(serializers.data)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    user = room.admin.user
    posts = Post.objects.filter(room=Room.objects.get(id=pk).code)
    print(posts)
    if request.user != user:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    posts.delete()
    room.delete()
    return Response(f'Room with id {pk} was deleted')

def getAdminRooms(pk):
    user = Profile.objects.get(id=pk)
    rooms = Room.objects.filter(admin=user)
    serialzers = RoomSerializer(rooms, many=True)
    return Response(serialzers.data)

def getCodeRoom(code):
    room = Room.objects.get(code=code)
    serializers = RoomSerializer(room, many=False)
    return Response(serializers.data)

def addByCode(code, user):
    room = Room.objects.get(code=int(code))
    profile = Profile.objects.get(user=user)
    member, created = RoomMember.objects.get_or_create(
        account = profile,
        room = room
    )
    serializers = RoomMemberSerializer(member, many=False)
    return Response(serializers.data)

def getUserRooms(pk):
    user = Profile.objects.get(id=pk)
    members = RoomMember.objects.filter(account=user)
    serializers = RoomMemberSerializer(members, many=True)
    return Response(serializers.data)

def getMemberRooms():
    members = RoomMember.objects.all()
    serializers = RoomMemberSerializer(members, many=True)
    return Response(serializers.data)

def getMemberRoom(pk):
    member = RoomMember.objects.get(id=pk)
    serializers = RoomMemberSerializer(member, many=False)
    return Response(serializers.data)

def deleteMemberRoom(request, pk):
    rmr = RoomMember.objects.get(id=pk) #rmr = room member relation
    admin = rmr.room.admin.user
    user = rmr.account.user
    if request.user != user and request.user != admin:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    rmr.delete()
    return Response(f'Room with id {pk} was deleted')

def getMemberRoomUser(pk, pk2):
    rmr = RoomMember.objects.get(room=pk, account=pk2)
    serializers = RoomMemberSerializer(rmr, many=False)
    return Response(serializers.data)

def getRoomMembers(pk):
    room = Room.objects.get(id=pk)
    rmr = RoomMember.objects.filter(room=room)
    serializers = RoomMemberSerializer(rmr, many=True)
    return Response(serializers.data)

def getRoomUsers(pk):
    try:
        room = Room.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Does not exist', status=status.HTTP_404_NOT_FOUND)
    rmr = RoomMember.objects.filter(room=room)
    users = Profile.objects.none()
    for i in rmr:
        print(i.account) 
        users |= Profile.objects.filter(id=i.account.id)
    serializers = ProfileSerializer(users, many=True)
    return Response(serializers.data)

def getRoomIncluded(pk):
    user = Profile.objects.get(id=pk)
    rooms = Room.objects.filter(admin=user)
    rmr = RoomMember.objects.filter(account=pk)
    for i in rmr:
        rooms |= Room.objects.filter(id=i.room.id)
    serialzers = RoomSerializer(rooms, many=True)
    return Response(serialzers.data)

def getRoomPosts(pk):
    room = Room.objects.get(id=pk)
    posts = Post.objects.filter(room=room.code)
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data)

class IsGetOrIsAuthenticated(BasePermission):
    """
    Determines whether a request can be allowed or not.
    """

    def has_permission(self, request, view):
        # Allow GET requests
        if request.method == 'GET':
            return True
        
        # Check if user is authenticated and allow access if so
        return request.user.is_authenticated
