from django.shortcuts import render
from .serializers import RegisterSerializer, BoardSerializer, TaskSerializer, UpdateTaskSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTaskOwner,IsBoardOwner
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
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	permission_classes = [IsTaskOwner]
	lookup_field = 'id'
	lookup_url_kwargs = 'board_id'
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name','description']

class AddTask(CreateAPIView):
	serializer_class = TaskSerializer
	permission_classes = [IsTaskOwner]
	# lookup_field = 'id'
	# lookup_url_kwargs = 'board_id'

	def perform_create(self,serializer):
		serializer.save(board_id=self.kwargs['board_id'])


class UpdateTask(RetrieveUpdateAPIView):
	queryset = Task.objects.all()
	serializer_class = UpdateTaskSerializer
	lookup_field = 'id'
	permission_classes = [IsTaskOwner]


class DeleteBoard(DestroyAPIView):
	queryset = Board.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'board_id'
	permission_classes=[IsBoardOwner]


class DeleteTask(DestroyAPIView):
	queryset = Task.objects.all()
	lookup_field = 'id'
	permission_classes=[IsTaskOwner]
