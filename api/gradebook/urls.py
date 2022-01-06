from django.urls import path, include
from gradebook import views
from rest_framework.routers import DefaultRouter


# Creates routes for all methods supported by the viewset.
router = DefaultRouter()


router.register('terms', views.TermViewSets)
router.register('subjects', views.SubjectViewSets)
router.register('classes', views.ClassViewSets)
router.register('periods', views.PeriodViewSets)
router.register('assignment-types', views.AssignmentTypesViewSets)
router.register('assignments', views.AssignmentViewSets)
router.register('scores', views.ScoreViewSets)


app_name = 'gradebook'


urlpatterns = [
    path('year', views.YearAPIView.as_view()),
    path('', include(router.urls))
    ]
