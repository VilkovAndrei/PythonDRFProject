from typing import Set
from django.contrib import admin
from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city')
    search_fields = ('email', 'phone')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }
        if not is_superuser and obj is not None and obj == request.user:
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'course', 'lesson', 'payment_amount', 'payment_method')
    search_fields = ('user', 'course', 'lesson')
