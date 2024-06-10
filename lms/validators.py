from rest_framework.serializers import ValidationError


class LessonUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, url):
        youtube = 'https://youtube.com/'

        if url and youtube not in url:
            raise ValidationError('Можно размещать только материалы, опубликованные на youtube')
        else:
            return None
