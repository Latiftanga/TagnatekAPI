from rest_framework import serializers
from gradebook import models


class YearSerializer(serializers.ModelSerializer):
    '''Year Serializer'''
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


class TermSerializer(serializers.ModelSerializer):
    '''Term Serializer'''
    class Meta:
        model = models.Term
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

    def create(self, validated_data):
        validated_data.pop('school', None)
        return models.Term.objects.create(**validated_data)


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


class PeriodSerializer(serializers.ModelSerializer):
    '''Period Serializer'''
    class Meta:
        model = models.Period
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'periods',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


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
        students = validated_data.pop('students', None)
        periods = validated_data.pop('periods', None)
        klass = models.Class.objects.create(**validated_data)
        if students:
            klass.students.add(students)
        if periods:
            klass.periods.add(periods)
        return klass


class ClassDetailSerializer(ClassSerializer):
    '''Class Students'''
    students = serializers.StringRelatedField(
        many=True,
        read_only=True
        )
    periods = serializers.StringRelatedField(
        many=True,
        read_only=True
        )


class AssignmentTypeSerializer(serializers.ModelSerializer):
    '''Class Assignment types serializer'''
    class Meta:
        model = models.AssignmentType
        fields = '__all__'
        read_only_fields = (
            'id',
            'school',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class AssignmentSerializer(serializers.ModelSerializer):
    '''Class assignment Serializers'''
    class Meta:
        model = models.Assignment
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
        return models.Assignment.objects.create(**validated_data)


class ScoreSerializer(serializers.ModelSerializer):
    '''Serializer for Assignment Scores'''
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ScoreSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = models.Score
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
        return models.Score.objects.create(**validated_data)
