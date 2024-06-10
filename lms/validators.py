from rest_framework.serializers import ValidationError


class LessonUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('url')
        youtube = 'youtube.com'
        if video_url and youtube not in video_url:
            raise ValidationError('Можно размещать только материалы, опубликованные на youtube')
        else:
            return None
