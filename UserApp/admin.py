from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, UserAddress
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'fullname', 'date_of_birth', 'account_creation_date',)
    list_filter = ('groups', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'bio', 'mobile', 'facebook_id', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_superuser', 'groups')}),
        ('Custom Permissions', {'fields': ('user_permissions',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'bio', 'mobile', 'facebook_id',
                       'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'fullname', 'mobile')
    ordering = ('email', 'fullname')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(UserAddress)
