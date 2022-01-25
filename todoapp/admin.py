from django.contrib import admin

from .models import Department, Master, Profile, profile_pic, connection, connectionRequet, ToDo, ToDoMember, ToDOparticipant


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'JObTitles')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'Email', 'Password', 'IsActive')
    list_filter = ('IsActive',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Birthdate',
        'Master',
        'department',
        'FullName',
        'JobTitle',
        'Mobile',
        'RefID',
        'Gender',
        'Country',
        'State',
        'City',
        'Address',
    )
    list_filter = ('Birthdate', 'Master', 'department')


@admin.register(profile_pic)
class profile_picAdmin(admin.ModelAdmin):
    list_display = ('id', 'Master', 'Img')
    list_filter = ('Master',)


@admin.register(connection)
class connectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'Master', 'profile', 'status')
    list_filter = ('Master', 'profile')


@admin.register(connectionRequet)
class connectionRequetAdmin(admin.ModelAdmin):
    list_display = ('id', 'Master', 'profile')
    list_filter = ('Master', 'profile')


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Deadline',
        'master',
        'Title',
        'Tags',
        'Description',
        'Iscomplete',
    )
    list_filter = ('Deadline', 'master', 'Iscomplete')


@admin.register(ToDoMember)
class ToDoMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'profile')
    list_filter = ('todo', 'profile')


@admin.register(ToDOparticipant)
class ToDOparticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'Connection')
    list_filter = ('todo', 'Connection')