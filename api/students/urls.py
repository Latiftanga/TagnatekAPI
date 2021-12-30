from django.urls import path, include
from students import views
from rest_framework.routers import DefaultRouter


# Creates routes for all methods supported by the viewset.
router = DefaultRouter()


# router.register('', views.StudentsViewSets)
router.register('programmes', views.ProgrammeViewSets)


app_name = 'students'


urlpatterns = [
    path('', include(router.urls))
    ]
