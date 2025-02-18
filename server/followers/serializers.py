from rest_framework import serializers

from main import models
from .models import FriendRequest
from author.serializers import AuthorProfileSerializer

class FollowersSerializer(serializers.ModelSerializer):
    followers = AuthorProfileSerializer(read_only=True, many=True)

    class Meta:
        model = models.Followers
        fields = ('followers',)

class FriendSerializer(serializers.ModelSerializer):
    following = AuthorProfileSerializer(read_only=True, many=True)

    class Meta:
        model = models.Author
        fields = ('following',)
class FollowersModificationSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    

    def get_followers(self, obj):
        context = self.context
        request = context.get("request")
        qs = request

        return qs
    class Meta:
        model = models.Followers
        fields = ('followers',)   


# class FriendSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = FriendRequest
#         summary = serializers.SerializerMethodField()
#         actor = serializers.SerializerMethodField()
#         object = serializers.SerializerMethodField()
        
#         def get_summary(self, obj):
#             return obj.summary()

#         def get_actor(self, obj):
#             return obj.actor()
        
#         def get_object(self, obj):
#             return obj.object()
        
#         fields = ('type', 'summary', 'actor', 'object')

class FollowersFriendSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()

    def get_friends(self, obj):
        friends = AuthorProfileSerializer(obj.friends(), many=True)
        return friends.data

    class Meta:
        model = models.Followers
        fields = ('friends',)
