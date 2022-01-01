from rest_framework import serializers
from students.models import (
    Programme, Class, House,
    Guardian, Student
    )


class ProgrammeSerializer(serializers.ModelSerializer):
    '''Programme model serializer'''

    class Meta:
        model = Programme
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class ProgrammeRelatedField(serializers.StringRelatedField):
    '''Related field '''
    def to_representation(self, value):
        return ProgrammeSerializer(value).data

    def to_internal_value(self, data):
        return data


class ClassSerializer(serializers.ModelSerializer):
    '''Class model serializer'''
    # programme = ProgrammeRelatedField()
    class Meta:
        model = Class
        fields = '__all__'
        read_only_fields = (
            'id',
            'name',
            'is_active',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )

    def create(self, validated_data):
        validated_data.pop('school', None)
        return Class.objects.create(**validated_data)


class HouseSerializer(serializers.ModelSerializer):
    '''Serializer for student Houses'''

    class Meta:
        model = House
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class GuaridianSerializer(serializers.ModelSerializer):
    '''Student serializer'''

    class Meta:
        model = Guardian
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'user',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class StudentSerializer(serializers.ModelSerializer):
    '''Student serializer'''

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'user',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class StudentImgUploadSerializer(serializers.ModelSerializer):
    '''Student image upload serializer'''
    class Meta:
        model = Student
        fields = ('id', 'image')
        read_only_fields = ('id', )
