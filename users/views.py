from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from users.models import User, Payment
from users.permissions import UserPermissionsDestroy, IsOwner
from users.serializers import (UserSerializer, PaymentSerializer, UserDetailSerializer, UserLimitedSerializer,
                               MyTokenObtainPairSerializer)

from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save(is_active=True)
        new_user.set_password(new_user.password)
        new_user.save()


class UserRetrieveView(generics.RetrieveAPIView):
    # serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.id == self.kwargs["pk"] or self.request.user.is_superuser:
            self.serializer_class = UserDetailSerializer
        else:
            self.serializer_class = UserLimitedSerializer
        return self.serializer_class


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserDestroyView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    permission_classes = [UserPermissionsDestroy]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['lesson', 'course', 'payment_method']
    ordering_fields = ['date']
    permission_classes = [IsOwner]


class PaymentRetrieveView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]


class PaymentUpdateView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]


class PaymentDestroyView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]
