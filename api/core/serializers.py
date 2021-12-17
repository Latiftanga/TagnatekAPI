from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.models import Role, Permission


class UserSerializer(serializers.ModelSerializer):
    """Serializer for converting user model object"""

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "role",
            "school",
            "last_login",
            "created",
            "created_by",
            "updated",
            "updated_by",
            "is_active",
            "is_staff",
            )
        read_only_fields = (
            'id',
            'last_login',
            'is_active',
            'is_staff',
            'created',
            'created_by',
            'updated',
            'updated_by',
            'role',
            'school'
            )
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
            }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        role = validated_data.pop('role', None)
        user = get_user_model().objects.create_user(**validated_data)
        if role is not None:
            role_obj = Role.objects.get(id=int(role))
            if role_obj:
                user.role = role_obj
            user.save()
        return user

    def update(self, instance, validated_data):
        """Update a user, setting password correctly and return it"""
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)

        user = super().update(instance, validated_data)
        if role:
            role_obj = Role.objects.get(id=int(role))
            if role_obj:
                user.role = role_obj
            user.save()
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password', 'trim_whitespace': False}
        )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
            )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    '''User Role model serializer'''

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'permissions',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', None)
        role = super().create(validated_data)

        if permissions:
            role.permissions.add(permissions)
            role.save()
        return role


class PermissionSerializer(serializers.ModelSerializer):
    '''User Permission Serializer'''
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to user profiles"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'image')
        read_only_fields = ('id',)
