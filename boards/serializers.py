from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from datetime import datetime

from .models import Board,Task

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['description', 'is_hidden', 'is_done']

class FullBoardSerializer(serializers.ModelSerializer):
    done_tasks = serializers.SerializerMethodField()
    not_done_tasks = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['title', 'owner','done_tasks','not_done_tasks']
    def get_done_tasks(self,obj):
        if obj.owner == self.context['request'].user:
            tasks = Task.objects.filter(board=obj,is_done=True)
        else:
            tasks = Task.objects.filter(board=obj,is_hidden=False,is_done=True)
        return TaskSerializer(tasks,many=True).data
    def get_not_done_tasks(self,obj):
        if obj.owner == self.context['request'].user:
            tasks = Task.objects.filter(board=obj,is_done=False)
        else:
            tasks = Task.objects.filter(board=obj,is_hidden=False,is_done=False)
        return TaskSerializer(tasks,many=True).data

class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_hidden']
