from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from lms.models import Lesson, Course, Subscription
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

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(email='user@test.com', password='1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        """Создание тестового курса"""
        self.course = Course.objects.create(name='Tests', description='Tests description', owner=self.user)

    def test_subscription_activate(self):
        url = reverse('lms:subscription_create')
        data = {'user': self.user.id,
                'course': self.course.id}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка добавлена'})

    def test_subscription_deactivate(self):
        url = reverse('lms:subscription_create')
        Subscription.objects.create(user=self.user, course=self.course)
        data = {'user': self.user.id,
                'course': self.course.id}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка удалена'})


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', password='123')
        self.course = Course.objects.create(name='Tests', description='Tests description', owner=self.user)
        self.lesson = Lesson.objects.create(name='Tests',
                                            description='Tests description',
                                            course=self.course,
                                            owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        url = reverse('lms:course-list')
        print(url)
        data = {
            'name': 'Тестовый курс',
            'description': 'Тестовый курс',
            'owner': self.user.pk
        }
        response = self.client.post(url, data)
        print(response)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_retrieve(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        print(response.json())
        self.assertEqual(
            data, {'name': 'Tests', 'preview': None, 'description': 'Tests description', 'owner': self.user.pk,
                   'lessons': [
                       {'id': self.lesson.pk, 'name': 'Tests', 'preview': None, 'description': 'Tests description',
                        'url': None, 'course': self.course.pk, 'owner': self.user.pk}],
                   'lesson_count': 1,
                   'is_signed': 'Не подписан'}
        )

    def test_course_update(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {
            'name': 'TESTupdate'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'TESTupdate'
        )

    def test_course_list(self):
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.course.pk, 'name': self.course.name, 'preview': None, 'description': self.course.description,
             'owner': self.user.pk, 'is_signed': 'Не подписан'}]}
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(data, result)

    def test_course_delete(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )
