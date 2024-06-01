from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentCreateView, PaymentListView, PaymentRetrieveView, \
    PaymentUpdateView, PaymentDestroyView, UserUpdateView, UserDetailView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'profile', UserViewSet, basename='profile')
urlpatterns = [
                  path('profile/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
                  path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
                  path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
                  path('payment/list/', PaymentListView.as_view(), name='payment_list'),
                  path('payment/view/<int:pk>/', PaymentRetrieveView.as_view(), name='payment_view'),
                  path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
                  path('payment/delete/<int:pk>/', PaymentDestroyView.as_view(), name='payment_delete'),
] + router.urls
