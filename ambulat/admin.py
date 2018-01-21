from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from ambulat.models import Speciality, UserProfile, Personnel, Curriculum, Patient, Ambcard
from django.contrib.auth.forms import AdminPasswordChangeForm
from ambulat.forms import RaiseIfNotRulePassword
from mysite.models import get_object_or_none


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = u'Профілі користувачей'


class CheckAdminPasswordChangeForm(AdminPasswordChangeForm):
    def clean_password1(self):
        pwd = self.cleaned_data.get("password1")
        RaiseIfNotRulePassword(pwd)
        return pwd

    '''	
    def save(self, commit=True):
        #
        raw_password = self.cleaned_data['password1']
        #
        return super(CheckAdminPasswordChangeForm, self).save(commit)
    '''


class PersonAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'date_joined', 'is_staff', 'is_superuser', 'groups')
    list_hierarhchy = 'date_joined'
    ordering = ('-date_joined',)
    inlines = (UserProfileInline, )
    change_password_form = CheckAdminPasswordChangeForm


class PersonGroupAdmin(GroupAdmin):
    list_display = ('name', 'get_group_staus_login')
    actions = ['login_group_users', 'unlogin_group_users']
    login_permission = get_object_or_none(Permission, codename='login_to_site')

    def login_group_users(self, request, queryset):
        if self.login_permission:
            for login_group in queryset:
                login_group.permissions.add(self.login_permission)
            self.message_user(request, u'Вхід до сайту дозволений для обраних груп.')
    login_group_users.short_description = u'Дозволити вхід до сайту для обраних груп'

    def unlogin_group_users(self, request, queryset):
        if self.login_permission:
            for login_group in queryset:
                login_group.permissions.remove(self.login_permission)
            self.message_user(request, u'Вхід до сайту заборонено для обраних груп.')
    unlogin_group_users.short_description = u'Заборонити вхід до сайту для обраних груп'

    def get_group_staus_login(self, obj):
        perm = obj.permissions.filter(codename='login_to_site')
        return u'Ні' if len(perm) == 0 else u'Так'
    get_group_staus_login.short_description = u'Вхід до сайту дозволений'


class MyAdminSite(admin.AdminSite):
    pass

my_site = MyAdminSite()

admin.site.unregister(User)
admin.site.unregister(Group)
my_site.register(Group, PersonGroupAdmin)
my_site.register(User, PersonAdmin)
# admin.site.unregister(User)
# admin.site.register(User, PersonAdmin)
my_site.register(Speciality)
# admin.site.register(UserProfile)
my_site.register(Personnel)
my_site.register(Curriculum)
my_site.register(Patient)
my_site.register(Ambcard)
