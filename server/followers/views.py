from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import generics, permissions, status

from main import models
from .models import FriendRequest
from inbox.models import Inbox
from followers.serializers import FollowersSerializer, FollowersModificationSerializer, FollowersFriendSerializer
from .serializers import FriendSerializer

#<slug:id>/followers/
class FollowersView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        requestAuthorId = self.kwargs['id']

        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        try: 
            authorExists = models.Followers.objects.filter(author=requestAuthorId).exists()
            if not authorExists:
                authorObj = models.Author.objects.get(id=requestAuthorId)
                models.Followers.objects.create(author=authorObj)
        except:
            raise ValidationError({"error": ["User not found"]})

        try:
            return models.Followers.objects.get(author=requestAuthorId)
        except:
            raise ValidationError({"error": ["User not found"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'type': 'followers',
            'items': serializer.data['followers'],
        })

#/<slug:id>/followers/<slug:foreignId>/
class FollowersModificationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FollowersModificationSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        self.requestAuthorId = self.kwargs['id']
        self.requestForeignAuthorId = self.kwargs['foreignId']
        
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        try :
            authorExists = models.Followers.objects.filter(author=self.requestAuthorId).exists()
            if not authorExists:
                authorObj = models.Author.objects.get(id=self.requestAuthorId)
                models.Followers.objects.create(author=authorObj)
        except:
            raise ValidationError({"error": ["User not found"]})


        try:
            self.author = models.Author.objects.get(id=self.requestAuthorId)
            self.foreignAuthor = models.Author.objects.get(id=self.requestForeignAuthorId)
                  
            return models.Followers.objects.filter(author=self.requestAuthorId)

        except:
            raise ValidationError({"error": ["User not found"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
                
        return Response({
            'type': 'follower',
            'items': [{
                'status': self.foreignAuthor in serializer.data['followers'],
                'author':  self.author.id,
                'follower': self.foreignAuthor.id,
            }]
        })

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.get_serializer(instance, data=request.data, partial=True)
        
        if (str(self.requestForeignAuthorId) != str(request.user.id)):
           return Response({
                'error': ['This is not your account, you cannot follow this author']}, status=status.HTTP_403_FORBIDDEN) 
        elif (self.requestAuthorId == self.requestForeignAuthorId):
            return Response({
                'error': ['You cannot follow yourself']}, status=status.HTTP_400_BAD_REQUEST)
        elif (not self.request.user.adminApproval):
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        
        authorObj = models.Author.objects.get(id=self.requestAuthorId)
        author = models.Followers.objects.get(author=authorObj)
        foreignAuthor = models.Author.objects.get(id=self.requestForeignAuthorId)

        author.followers.add(foreignAuthor)
        author.save()

        friend_request = FriendRequest.objects.filter(follower=foreignAuthor, author=authorObj)
        if not friend_request:
            create_friend_request = FriendRequest.objects.create(follower=foreignAuthor, author=authorObj)
            friend_request_obj = FriendRequest.objects.get(follower=foreignAuthor, author=authorObj)
            friend_request_text = FriendSerializer(friend_request_obj).data
            inbox = Inbox.objects.get(author=authorObj)
            inbox.items.append(friend_request_text)
            inbox.save()
        
        return Response({
            'type': 'follow',
            'items': [{
                'status': True,
                'author':  self.author.id,
                'follower': self.foreignAuthor.id,
            }]
        })
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            raise ValidationError({"error": ["User not found"]})

        if (str(self.requestForeignAuthorId) != str(request.user.id)):
           return Response({
                'error': ['This is not your account, you cannot unfollow this author']}, status=status.HTTP_403_FORBIDDEN) 
        elif (self.requestAuthorId == self.requestForeignAuthorId):
            return Response({
                'error': ['You cannot unfollow yourself']}, status=status.HTTP_400_BAD_REQUEST)
        elif (self.foreignAuthor not in serializer.data['followers']):
            return Response({
                'error': ['You are not following this author, hence, you can unfollow']}, status=status.HTTP_400_BAD_REQUEST)
        elif (not self.request.user.adminApproval):
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})


        authorObj = models.Author.objects.get(id=self.requestAuthorId)
        author = models.Followers.objects.get(author=authorObj)
        foreignAuthor = models.Author.objects.get(id=self.requestForeignAuthorId)

        author.followers.remove(foreignAuthor)
        author.save()

        FriendRequest.objects.filter(follower=foreignAuthor, author=authorObj).delete()

        return Response({
            'type': 'unfollow',
            'items': [{
                'status': False,
                'author':  author.author.id,
                'follower': foreignAuthor.id,
            }]
        })

class FollowersFriendView(generics.RetrieveAPIView):
    serializer_class = FollowersFriendSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        author_id = self.kwargs['id']
        try:
            query = models.Followers.objects.get(author=author_id)
        except:
            query = None
        return query
