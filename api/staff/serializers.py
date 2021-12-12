from rest_framework.serializers import ModelSerializer
from core.permissions import StaffPermission
from rest_framework.authentication import TokenAuthentication
from core.authentication import JWTAuthentication
from staff.models import (
    Qualification,
    Department,
    Staff
    )


class DepartmentSerializer(ModelSerializer):
    '''Staff Department Serializer'''

    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication
        )
    permission_classes = (StaffPermission, )

    class Meta:
        model = Department,
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class QualificationSerializer(ModelSerializer):
    '''Staff Qualification Serializer'''

    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication
        )
    permission_classes = (StaffPermission, )

    class Meta:
        model = Qualification,
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class StaffSerializer(ModelSerializer):
    '''Staff Serializer'''

    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication
        )
    permission_classes = (StaffPermission, )

    class Meta:
        model = Staff,
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )
