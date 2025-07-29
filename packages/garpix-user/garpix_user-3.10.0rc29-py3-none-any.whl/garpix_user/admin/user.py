from garpix_utils.cef_logs.event import UserUpdateEvent
from garpix_utils.cef_logs.mixins.create_log import CreateLogMixin
from garpix_utils.models import AdminDeleteMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from garpix_user.utils.get_password_settings import get_password_settings


class UserAdmin(AdminDeleteMixin, BaseUserAdmin, CreateLogMixin):
    change_form_template = "garpix_user/send_confirm.html"

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_deleted', 'is_staff', 'is_superuser',
                'is_blocked', 'login_attempts_count', 'password_updated_date', 'needs_password_update',
                'groups', 'user_permissions', 'keycloak_auth_only'
            ),
        }),
        (_('Viber'), {
            'fields': ('viber_chat_id', 'viber_secret_key',)
        }),
        (_('Telegram'), {
            'fields': ('telegram_chat_id', 'telegram_secret', 'get_telegram_connect_user_help'),
        }),
        (_('Confim information'), {
            'fields': (
                'is_email_confirmed', 'email_confirmation_code', 'is_phone_confirmed', 'phone_confirmation_code'),
        }),
    )
    readonly_fields = ['telegram_secret', 'get_telegram_connect_user_help'] + list(BaseUserAdmin.readonly_fields)

    def delete_model(self, request, obj):
        event, params = self.log_delete(request, obj)
        super().delete_model(request, obj)
        event(**params)

    def delete_queryset(self, request, queryset):
        events = []
        for obj in queryset:
            events.append(self.log_delete(request, obj))
        super().delete_queryset(request, queryset)
        for event, params in events:
            event(**params)

    def save_model(self, request, obj, form, change):
        password_first_change = get_password_settings()['password_first_change']

        if not change and password_first_change:
            obj.needs_password_update = True

        events = self.logs_change_or_create(request, obj, change)
        for event, params in events:
            event(**params)
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        obj = form.instance
        prev_groups, prev_permissions = set(), set()
        if change:
            prev_groups = set([str(_obj) for _obj in obj.groups.all()])
            prev_permissions = set([str(_obj) for _obj in obj.user_permissions.all()])
            events = self.logs_change_m2m_field(request, super(), form, formsets, change,
                                                exclude_fields=['groups', 'user_permissions'])
            for event, params in events:
                event(**params)

        else:
            super().save_related(request, form, formsets, change)

        groups = set([str(_obj) for _obj in obj.groups.all()])
        permissions = set([str(_obj) for _obj in obj.user_permissions.all()])

        new_old_groups = groups - prev_groups
        old_new_groups = prev_groups - groups

        new_old_permissions = permissions - prev_permissions
        old_new_permissions = prev_permissions - permissions

        events = []

        if new_old_groups or old_new_groups:
            if new_old_groups:
                msg = f'Пользователь {str(obj)}(id={obj.pk}) был добавлен в группы {new_old_groups}'
                events.append((UserUpdateEvent(), msg))
            if old_new_groups:
                msg = f'Пользователь {str(obj)}(id={obj.pk}) был удален из групп {old_new_groups}'
                events.append((UserUpdateEvent(), msg))

        msg = CreateLogMixin.log_msg_change if CreateLogMixin.log_msg_change else f'Привилегии пользователя {str(obj)}(id={obj.pk}) были изменены'

        changed_fields = ''
        if new_old_permissions or old_new_permissions:
            if new_old_permissions:
                changed_fields += f'+добавлены {new_old_permissions} '
            if old_new_permissions:
                changed_fields += f'-удалены {old_new_permissions} '

            events.append((UserUpdateEvent(), msg))

        for event, message in events:
            event(request=request, user=request.user, msg=message)
