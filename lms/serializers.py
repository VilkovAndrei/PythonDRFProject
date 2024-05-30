from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'owner', 'lesson_count')

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
