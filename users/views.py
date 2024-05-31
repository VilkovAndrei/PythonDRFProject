from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# class PaymentViewSet(viewsets.ModelViewSet):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#     filter_backends = [OrderingFilter, DjangoFilterBackend]
#     # search_fields = ['user', 'course']
#     ordering_fields = ['date',]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['lesson', 'course', 'payment_method']
    ordering_fields = ['date',]


class PaymentRetrieveView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentUpdateView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
