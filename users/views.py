from rest_framework import viewsets, generics, serializers
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from users.models import User, Payment
from users.permissions import UserPermissionsDestroy, IsOwner
from users.serializers import (UserSerializer, PaymentSerializer, UserDetailSerializer, UserLimitedSerializer,
                               MyTokenObtainPairSerializer, PaymentRetrieveSerializer)

from rest_framework_simplejwt.views import TokenObtainPairView

from users.services import create_stripe_product, create_stripe_price, create_stripe_session, convert_rub_to_usd, \
    convert_currency


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

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        lesson = serializer.validated_data.get('lesson')
        if not course and not lesson:
            raise serializers.ValidationError('Course or lesson is required.')
        payment = serializer.save()
        payment.payment_amount = 0
        if course:
            payment.payment_amount = course.amount
        elif lesson:
            payment.payment_amount = lesson.amount
        payment.user = self.request.user
        if payment.payment_method == 'NON_CASH':
            stripe_product_id = create_stripe_product(payment)
            price_usd = convert_currency(payment.payment_amount)
            price = create_stripe_price(summ=price_usd, stripe_product_id=stripe_product_id)
            session_id, payment_link, payment_status = create_stripe_session(price=price)
            payment.session_id = session_id
            payment.payment_url = payment_link
            payment.payment_status = payment_status
        payment.save()
        return super().perform_create(serializer)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['lesson', 'course', 'payment_method']
    ordering_fields = ['date']
    permission_classes = [IsAuthenticated]


class PaymentRetrieveView(generics.RetrieveAPIView):
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentUpdateView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]


class PaymentDestroyView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]
