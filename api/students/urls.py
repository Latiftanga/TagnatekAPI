from django.urls import path, include
from students import views
from rest_framework.routers import DefaultRouter


# Creates routes for all methods supported by the viewset.
router = DefaultRouter()


router.register('programmes', views.ProgrammeViewSets)
router.register('classes', views.ClassViewSets)
router.register('houses', views.HouseViewSets)
router.register('', views.StudentsViewSets)


app_name = 'students'


urlpatterns = [
    path('', include(router.urls))
    ]
