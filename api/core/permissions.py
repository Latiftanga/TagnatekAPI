from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_staff
        return False


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role.name == 'teacher'\
            or request.user.role.name == 'admin' \
            or request.user.role.name == 'super'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role.name == 'teacher'\
            or request.user.role.name == 'admin' \
            or request.user.role.name == 'super' \
            or request.user.role.name == 'student'
        


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'parent'
