from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    fieldsets = (
        (None, {
            'fields': ('title',  'text')
        }),
    )
    list_display = ['title', 'author', 'pub_date' ]


admin.site.register(Notification, NotificationAdmin)
