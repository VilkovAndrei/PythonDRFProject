from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter

from lms.views import CourseViewSet, LessonCreateView, LessonListView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
                  path('lesson/list/', LessonListView.as_view(), name='lesson_list'),
                  path('lesson/view/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_view'),
                  path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete'),

              ] + router.urls
