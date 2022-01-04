from django.db.models import Q
from django.db.models.query_utils import refs_expression
from rest_framework import serializers
from gradebook import models


class YearSerializer(serializers.ModelSerializer):
    '''Subject Serializer'''
    class Meta:
        model = models.Year
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'is_active',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class SubjectSerializer(serializers.ModelSerializer):
    '''Subject Serializer'''
    class Meta:
        model = models.Subject
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )

    def create(self, validated_data):
        validated_data.pop('school', None)
        return models.Subject.objects.create(**validated_data)


class ClassSerializer(serializers.ModelSerializer):
    '''Class Serializer'''
    class Meta:
        model = models.Class
        fields = '__all__'
        read_only_fields = (
            'id',
            'name',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )

    def create(self, validated_data):
        validated_data.pop('school', None)
        validated_data.pop('students', None)
        return models.Class.objects.create(**validated_data)

    def validate(self, data):
        '''Validate Subject'''
        try:
            klass = models.Class.objects.get(
                subject=data['subject'],
                term=data['term'],
                subject_type=data['subject_type']
                )
        except models.Class.DoesNotExist:
            klass = None

        if klass:
            raise serializers.ValidationError(
                f'{klass.subject_type} {klass.subject.name} exists'
                )
        return data
