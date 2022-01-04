from django.urls import path, include
from gradebook import views
from rest_framework.routers import DefaultRouter


# Creates routes for all methods supported by the viewset.
router = DefaultRouter()


router.register('years', views.YearViewSets)
router.register('subjects', views.SubjectViewSets)
router.register('classes', views.ClassViewSets)


app_name = 'gradebook'


urlpatterns = [
    path('', include(router.urls))
    ]
