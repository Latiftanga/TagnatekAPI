from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permissions import IsTeacher
from gradebook.serializers import (
    YearSerializer, TermSerializer
    )
from core.permissions import IsStaff
from core.views import CRUDViewSets
from gradebook import serializers, models


class TermViewSets(CRUDViewSets):
    queryset = models.Term.objects.all()
    serializer_class = TermSerializer


class YearAPIView(APIView):
    '''Academic Year Viewsets'''

    def get(self, request, format=None):
        try:
            current_year = models.Year.objects.get(
                school=request.user.school,
                is_active=True
                )
        except models.Year.DoesNotExist:
            current_year = None

        if current_year:
            return Response(YearSerializer(current_year).data)
        else:
            return Response(
                {'msg': 'Not found'}, status=status.HTTP_404_NOT_FOUND
                )

    def post(self, request, format=None):
        '''Creating new year'''
        try:
            current_year = models.Year.objects.get(
                school=request.user.school,
                is_active=True
                )
        except models.Year.DoesNotExist:
            current_year = None

        serializer = YearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                school=request.user.school,
                created_by=request.user.email
                )
            if current_year:
                current_year.is_active = False
                current_year.updated_by = request.user.email
                current_year.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )


class SubjectViewSets(CRUDViewSets):
    '''Subject Viewsets'''
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (IsStaff, )


class PeriodViewSets(CRUDViewSets):
    '''Periods Viewsets'''
    queryset = models.Period.objects.all()
    serializer_class = serializers.PeriodSerializer
    permission_classes = (IsStaff, )


class ClassViewSets(CRUDViewSets):
    '''Class Viewsets'''
    queryset = models.Class.objects.all()
    serializer_class = serializers.ClassSerializer
    permission_classes = (IsStaff, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ClassDetailSerializer
        return self.serializer_class


class AssignmentViewSets(CRUDViewSets):
    '''Viewset for Assignments'''
    queryset = models.Assignment.objects.all()
    serializer_class = serializers.AssignmentSerializer
    permission_classes = (IsTeacher,)


class AssignmentTypesViewSets(CRUDViewSets):
    '''Viewsets for Assignment Types'''
    queryset = models.AssignmentType.objects.all()
    serializer_class = serializers.AssignmentTypeSerializer
    permission_classes = (IsTeacher,)


class ScoreViewSets(CRUDViewSets):
    '''Viewsets for Assignment Scores'''
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer
    permission_classes = (IsTeacher,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED, headers=headers
            )
