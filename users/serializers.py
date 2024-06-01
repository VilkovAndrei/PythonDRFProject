from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    payments = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar', 'payments')

    def get_payments(self, instance):
        return PaymentSerializer(Payment.objects.filter(user=instance), many=True).data
