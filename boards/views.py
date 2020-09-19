from django.shortcuts import render
from .serializers import RegisterSerializer, FullBoardSerializer, TaskSerializer, UpdateTaskSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly,IsBoardOwnerOrReadOnly
from .models import Board,Task
from rest_framework.filters import OrderingFilter


class Register(CreateAPIView):
	serializer_class = RegisterSerializer

class CreateBoard(CreateAPIView):
	serializer_class = FullBoardSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class BoardsList(ListAPIView):
	queryset = Board.objects.all()
	serializer_class = FullBoardSerializer
	filter_backends = [OrderingFilter]
	ordering_fields = ['creation_date']

class AddTask(CreateAPIView):
	serializer_class = TaskSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def perform_create(self,serializer):
		serializer.save(board_id=self.kwargs['board_id'])


class UpdateTask(RetrieveUpdateAPIView):
	queryset = Task.objects.all()
	serializer_class = UpdateTaskSerializer
	lookup_field = 'id'
	permission_classes = [IsOwnerOrReadOnly]


class DeleteBoard(DestroyAPIView):
	queryset = Board.objects.all()
	lookup_field = 'id'
	permission_classes=[IsBoardOwnerOrReadOnly]


class DeleteTask(DestroyAPIView):
	queryset = Task.objects.all()
	lookup_field = 'id'
	permission_classes=[IsOwnerOrReadOnly]
