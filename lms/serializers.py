from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson
from lms.validators import LessonUrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        validators = [LessonUrlValidator(field='url')]
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'owner')


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'owner', 'lessons', 'lesson_count')

    @staticmethod
    def get_lesson_count(instance):
        return Lesson.objects.filter(course=instance).count()

    @staticmethod
    def get_lessons(instance):
        return LessonSerializer(Lesson.objects.filter(course=instance), many=True).data
