from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'student'


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'parent'
