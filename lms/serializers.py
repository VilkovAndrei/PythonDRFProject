from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import LessonUrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        extra_kwargs = {'url': {'required': False}}
        validators = [LessonUrlValidator(field='url')]
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    is_signed = SerializerMethodField()

    def get_is_signed(self, obj):
        request = self.context.get('request')
        user = None
        if request:
            user = request.user
        if Subscription.objects.filter(user=user).filter(course=obj.pk).exists():
            return "Подписан"
        return "Не подписан"

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'owner', 'is_signed')


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = SerializerMethodField()
    is_signed = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'owner', 'lessons', 'lesson_count', 'is_signed')

    @staticmethod
    def get_lesson_count(instance):
        return Lesson.objects.filter(course=instance).count()

    @staticmethod
    def get_lessons(instance):
        return LessonSerializer(Lesson.objects.filter(course=instance), many=True).data

    def get_is_signed(self, obj):
        request = self.context.get('request')
        user = None
        if request:
            user = request.user
        if Subscription.objects.filter(user=user).filter(course=obj.pk).exists():
            return "Подписан"
        return "Не подписан"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
