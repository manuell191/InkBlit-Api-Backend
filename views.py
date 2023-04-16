from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import (getUser, createUser, getUsers, updateUser, getLogin, deleteUser, 
        getFollows, createFollow, getFollow, deleteFollow, getUserFollows, getFollowingUser,
        getPosts, createPost, getUserPosts, getPost, deletePost, getRooms, createRoom,
        getRoom, deleteRoom, getAdminRooms, addById, getCodeRoom, addByCode, getUserRooms,
        getMemberRooms, getMemberRoom, deleteMemberRoom, getRoomMembers, getFollowingUserPosts,
        getRoomIncluded, createRoomPost, getRoomPosts, getRoomUsers, getUserProtected,
        getFollowingUserList, getUserFollowsList, getFollowingUserAccount, getMemberRoomUser)
from .utils import IsGetOrIsAuthenticated

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/user/',
            'method': 'GET',
            'description': 'Returns array of users'
        },
        {
            'Endpoint': '/user/',
            'method': 'POST',
            'body': {
                'username': "",
                'email': "",
                'password': "",
                'bio': ""
            },
            'description': 'Create new user'
        },
        {
            'Endpoint': '/user/<id>/protected',
            'method': 'GET',
            'head': {
                'Authentication': 'Token <token>'
            },
            'description': 'Get user data while requiring auth'
        },
        {
            'Endpoint': '/user/<id>/',
            'method': 'GET',
            'description': 'Get user info'
        },
        {
            'Endpoint': '/user/<id>/',
            'method': 'PUT',
            'headers': {
                'Authentication': 'Token <token>'
            },
            'body': {
                'username': "",
                'email': "",
                'password': "",
                'bio': ""
            },
            'description': 'Update user info'
        },
        {
            'Endpoint': '/user/<id>/',
            'method': 'DELETE',
            'headers': {
                'Authentication': 'Token <token>'
            },
            'description': 'Delete user'
        },

        {
            'Endpoint': '/follow/',
            'method': 'GET',
            'description': 'Get all follows'
        },
        {
            'Endpoint': '/follow/',
            'method': 'POST',
            'body': {
                'account': "",
                'following': ""
            },
            'description': 'Create new following relationship'
        },
        {
            'Endpoint': '/follow/<id>/',
            'method': 'GET',
            'description': 'Get follow relationship by id'
        },
        {
            'Endpoint': '/follow/<id>/',
            'method': 'DELETE',
            'headers': {
                'Authentication': 'Token <token>'
            },
            'description': 'Delete following relationship'
        },
        {
            'Endpoint': '/follows/<userid>/',
            'method': 'GET',
            'description': 'Get all users that this user follows'
        },
        {
            'Endpoint': '/following/<userid>/',
            'method': 'GET',
            'description': 'Get all users following this user'
        },
        {
            'Endpoint': '/folowing/<userid>/posts/',
            'method': 'GET',
            'description': 'Get all posts from users that this user follows'
        },

        {
            'Endpoint': '/post/',
            'method': 'GET',
            'description': 'Get all posts'
        },
        {
            'Endpoint': '/post/',
            'method': 'POST',
            'header': {
                'Authorization': 'Token <token>'
            },
            'body': {
                'content': ""
            },
            'description': 'Create new post'
        },
        {
            'Endpoint': '/post/user/<userid>/',
            'method': 'GET',
            'description': 'Get all posts from user'
        },
        {
            'Endpoint': '/post/<id>/',
            'method': 'GET',
            'description': 'Get a single post by id'
        },
        {
            'Endpoint': '/post/<id>/',
            'method': 'DELETE',
            'header': {
                'Authorization': 'Token <token>'
            },
            'description': 'Delete a post'
        },
        {
            'Endpoint': '/post/room/<roomid>/',
            'method': 'POST',
            'header': {
                'Authorization': 'Token <token>'
            },
            'body': {
                'content': ""
            },
            'description': 'Post to a room'
        },

        {
            'Endpoint': '/room/',
            'method': 'GET',
            'description': 'Get all rooms'
        },
        {
            'Endpoint': '/room/',
            'method': 'POST',
            'body': {
                'admin': ""
            },
            'description': 'Create room and add user as admin'
        },
        {
            'Endpoint': '/room/<id>/',
            'method': 'GET',
            'description': 'Get info about a room'
        },
        {
            'Endpoint': '/room/<id>',
            'method': 'POST',
            'description': 'Add a member to a room'
        },
        {
            'Endpoint': '/room/<id>/',
            'method': 'DELETE',
            'headers': {
                'Authorization': 'Token <token>'
            },
            'description': 'Delete a room'
        },
        {
            'Endpoint': '/room/admin/<userid>',
            'method': 'GET',
            'description': 'Get rooms that user is admin of'
        },
        
        {
            'Endpoint': '/room/code/<code>',
            'method': 'GET',
            'description': 'Get rooms by the code'
        },
        {
            'Endpoint': '/room/code/<code>',
            'method': 'POST',
            'description': 'Add a member to a room'
        },
        {
            'Endpoint': '/room/member/user/<userid>',
            'method': 'GET',
            'description': 'Get rooms that user is in'
        },
        {
            'Endpoint': '/room/member',
            'method': 'GET',
            'description': 'Get all room member relationships'
        },
        {
            'Endpoint': '/room/member/<id>',
            'method': 'GET',
            'description': 'Get a room member relationship by id'
        },
        {
            'Endpoint': '/room/member/<id>',
            'method': 'DELETE',
            'description': 'Delete a room member relationship'
        },
        {
            'Endpoint': '/room/<id>/users',
            'method': 'GET',
            'description': 'Get all users that are in room'
        },
        {
            'Endpoint': '/room/included/<userid>',
            'method': 'GET',
            'description': 'Get all rooms that user is included in'
        },
        {
            'Endpoint': '/room/<id>/posts',
            'method': 'GET',
            'description': 'Get all posts that room is included in'
        }
    ]
    return Response(routes)

#/login/
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        return getLogin(request.data)

#/users/
@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        return getUsers()
    elif request.method == 'POST':
        return createUser(request.data) 
    
#/user/<id>/protected/
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def userProtected(request, pk):
    if request.method == 'GET':
        return getUserProtected(pk, request.user)

#/user/<id>/
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def user(request, pk):
    if request.method == 'GET':
        return getUser(pk)
    elif request.method == 'PUT':
        return updateUser(request, pk)
    elif request.method == 'DELETE':
        return deleteUser(request, pk)



#/follow/
@api_view(['GET', 'POST'])
def follows(request):
    if request.method == 'GET':
        return getFollows()
    elif request.method == 'POST':
        return createFollow(request.data)
    
#/follow/<id>/
@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def follow(request, pk):
    if request.method == 'GET':
        return getFollow(pk)
    elif request.method == 'DELETE':
        return deleteFollow(request, pk)

#/follows/<userid>/
@api_view(['GET'])
def userFollows(request, pk):
    if request.method == 'GET':
        return getUserFollows(pk)

#/follows/<userid>/list/
@api_view(['GET'])
def userFollowsList(request, pk):
    if request.method == 'GET':
        return getUserFollowsList(pk)

#/following/<userid>/
@api_view(['GET'])
def followingUser(request, pk):
    if request.method == 'GET':
        return getFollowingUser(pk)

#/following/<userid>/list
@api_view(['GET'])
def followingUserList(request, pk):
    if request.method == 'GET':
        return getFollowingUserList(pk)

#/following/<userid>/posts/
@api_view(['GET'])
def followingUserPosts(request, pk):
    if request.method == 'GET':
        return getFollowingUserPosts(pk)

#/following/<userid>/account/<userid2>
@api_view(['GET'])
def followingUserAccount(request, pk, pk2):
    if request.method == 'GET':
        return getFollowingUserAccount(pk, pk2)



#/post/
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def posts(request):
    if request.method == 'GET':
        return getPosts()
    elif request.method == 'POST':
        return createPost(request.data, request.user)

#/post/user/<userid>/
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def userPosts(request, pk):
    if request.method == 'GET':
        return getUserPosts(pk, request.user)

#/post/<id>/
@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def post(request, pk):
    if request.method == 'GET':
        return getPost(pk)
    elif request.method == 'DELETE':
        return deletePost(request, pk)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def roomPost(request, pk):
    if request.method == 'POST':
        return createRoomPost(request.data, request.user, pk)



#/room/
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def rooms(request):
    if request.method == 'GET':
        return getRooms()
    elif request.method == 'POST':
        return createRoom(request.data, request.user)

#/room/<id>/
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def room(request, pk):
    if request.method == 'GET':
        return getRoom(pk)
    elif request.method == 'POST':
        return addById(request.data, pk)
    elif request.method == 'DELETE':
        return deleteRoom(request, pk)

#/room/admin/<userid>/
@api_view(['GET'])
def adminRooms(request, pk):
    if request.method == 'GET':
        return getAdminRooms(pk)

#/room/code/<code>/
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def codeRoom(request, pk):
    if request.method == 'GET':
        return getCodeRoom(pk)
    elif request.method == 'POST':
        return addByCode(pk, request.user)

#/room/member/user/<userid>/
@api_view(['GET'])
def userRooms(request, pk):
    if request.method == 'GET':
        return getUserRooms(pk)

#/room/member/
@api_view(['GET'])
def memberRooms(request):
    if request.method == 'GET':
        return getMemberRooms()

#/room/member/<id>/
@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsGetOrIsAuthenticated])
def memberRoom(request, pk):
    if request.method == 'GET':
        return getMemberRoom(pk)
    elif request.method == 'DELETE':
        return deleteMemberRoom(request, pk)

#/room/member/<id>/user<userId>
@api_view(['GET'])
def memberRoomUser(request, pk, pk2):
    if request.method == 'GET':
        return getMemberRoomUser(pk, pk2)

#/room/members/<id>/
@api_view(['GET'])
def roomMembers(request, pk):
    if request.method == 'GET':
        return getRoomMembers(pk)

#/room/<id>/users/
@api_view(['GET'])
def roomUsers(request, pk):
    if request.method == 'GET':
        return getRoomUsers(pk)

#/room/included/<id>/
@api_view(['GET'])
def roomIncluded(request, pk):
    if request.method == 'GET':
        return getRoomIncluded(pk)

@api_view(['GET'])
def roomPosts(request, pk):
    if request.method == 'GET':
        return getRoomPosts(pk)