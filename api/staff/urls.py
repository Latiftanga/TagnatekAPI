from django.urls import path, include
from staff import views
from rest_framework.routers import DefaultRouter


# Creates routes for all methods supported by the viewset.
router = DefaultRouter()


router.register('departments', views.DepartmentViewSets)


app_name = 'staff'


urlpatterns = [
    path('', include(router.urls))
    ]
