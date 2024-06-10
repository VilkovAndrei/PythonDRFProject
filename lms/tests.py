from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from lms.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(id=1, email='user@test.com', password='1234')
        self.client.force_authenticate(user=self.user)
        """Создание тестовых курса и урока"""
        self.course = Course.objects.create(name='test_course', description='test_description', owner=self.user)
        self.lesson = Lesson.objects.create(name='test_lesson', description='test_description',
                                            course=self.course, url='https://youtube.com/test/',
                                            owner=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        url = reverse('lms:lesson_create')
        data = {'name': 'Creating_test', 'description': 'Creating_test',
                'course': self.course.id, 'url': 'https://youtube.com/test/',
                'owner': self.user.id}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name=data['name']).exists())
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_retrieve_lesson(self):
        """Тестирование просмотра информации об уроке"""
        path = reverse('lms:lesson_view', [self.lesson.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        path = reverse('lms:lesson_update', [self.lesson.id])
        data = {'name': 'Updating_test', 'description': 'Updating_test'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, data['name'])

    def test_delete_lesson(self):
        admin = User.objects.create(id=2, email='admin@test.com',
                                    password='1234')
        self.client.force_authenticate(user=admin)

        path = reverse('lms:lesson_delete', [self.lesson.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
