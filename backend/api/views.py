from django.shortcuts import render
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializers,NoteSerializers
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Note

# create and return list
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author = user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author = self.request.user)
        else:
            print(serializer.errors)
            
class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author = user)

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'User with this username already exists.'})
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


