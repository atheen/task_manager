from django.shortcuts import render
from .serializers import RegisterSerializer, BoardSerializer, TaskSerializer, UpdateTaskSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import Board,Task
from rest_framework.filters import SearchFilter,OrderingFilter



class Register(CreateAPIView):
	serializer_class = RegisterSerializer

class CreateBoard(CreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BoardsList(ListAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer
	# filter_backends = [SearchFilter, OrderingFilter]
	# search_fields = ['name','description']

class TaskList(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'
    lookup_url_kwargs = 'board_id'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','description']

class AddTask(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'
    lookup_url_kwargs = 'board_id'

class UpdateTask(RetrieveUpdateAPIView):
    serializer_class = UpdateTaskSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'
    lookup_url_kwargs = 'task_id'
