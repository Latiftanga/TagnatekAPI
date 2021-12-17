from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from staff.models import (
    Qualification,
    Department,
    Staff,
    Job
    )


class DepartmentSerializer(ModelSerializer):
    '''Staff Department Serializer'''

    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'created',
            'created_by',
            'updated',
            'updated_by'
            ]
        read_only_fields = [
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            ]


class JobSerializer(ModelSerializer):
    '''Staff Jobs serializer'''

    class Meta:
        model = Job
        fields = [
            'id',
            'department',
            'description',
            'institution',
            'start_date',
            'end_date',
            'is_current',
            'created',
            'created_by',
            'updated',
            'updated_by'
            ]
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class QualificationSerializer(ModelSerializer):
    '''Staff Qualification Serializer'''

    class Meta:
        model = Qualification
        fields = [
            'id',
            'title',
            'institution',
            'date_admitted',
            'date_completed',
            'created',
            'created_by',
            'updated',
            'updated_by'
            ]
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class StaffSerializer(ModelSerializer):
    '''Staff Serializer'''

    class Meta:
        model = Staff
        fields = [
            'id',
            'first_name',
            'last_name',
            'other_names',
            'gender',
            'staff_id',
            'registered_no',
            'sssnit_no',
            'work_phone',
            'mobile_phone',
            'email',
            'jobs',
            'user',
            'school',
            'qualifications',
            'created',
            'created_by',
            'updated',
            'updated_by'
            ]
        read_only_fields = (
            'id',
            'school',
            'user',
            'qualifications',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )


class StaffDetailSerializer(StaffSerializer):
    qualifications = QualificationSerializer(
        read_only=True, many=True
        )
    jobs = serializers.StringRelatedField(many=True)
