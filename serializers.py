from rest_framework.serializers import ModelSerializer
from .models import Profile, Follow, Post, Room, RoomMember

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'bio'] #change for production

class UpdateProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio']

class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'account', 'following']
    
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'account', 'username', 'content', 'room']

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'code', 'admin']

class RoomMemberSerializer(ModelSerializer):
    class Meta:
        model = RoomMember
        fields = ['id', 'account', 'room']