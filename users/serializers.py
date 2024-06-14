from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment
from users.services import get_paymant_stripe_status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'city')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payment_status_now = SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('date', 'course', 'lesson', 'payment_amount', 'payment_method', 'payment_status_now')

    @staticmethod
    def get_payment_status_now(instance):
        if instance.session_id:
            instance.payment_stripe_status = get_paymant_stripe_status(instance.session_id)
            # print(instance.payment_stripe_status)
            instance.payment_status = instance.payment_stripe_status
            instance.save()
        return instance.payment_status


class UserDetailSerializer(serializers.ModelSerializer):
    payments = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar', 'payments')

    @staticmethod
    def get_payments(instance):
        return PaymentSerializer(Payment.objects.filter(user=instance), many=True).data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['email'] = user.email

        return token
