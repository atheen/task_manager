from rest_framework import permissions


class IsBoardOwnerOrReadOnly(permissions.BasePermission):
    message = "This isn't your board....."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "This isn't your board....."

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user
