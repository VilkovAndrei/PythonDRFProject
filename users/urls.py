from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentCreateView, PaymentListView, PaymentRetrieveView, \
    PaymentUpdateView, PaymentDestroyView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'profile', UserViewSet, basename='profile')
urlpatterns = [
                  path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
                  path('payment/list/', PaymentListView.as_view(), name='payment_list'),
                  path('payment/view/<int:pk>/', PaymentRetrieveView.as_view(), name='payment_view'),
                  path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
                  path('payment/delete/<int:pk>/', PaymentDestroyView.as_view(), name='payment_delete'),
] + router.urls
# router2 = DefaultRouter()
# router2.register(r'payment', PaymentViewSet, basename='payment')
# urlpatterns += router2.urls
