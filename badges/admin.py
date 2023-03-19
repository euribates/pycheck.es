from django.contrib import admin

from badges.models import Achievement, Badge


class AchievementAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('name', 'symbol', 'logic')
    list_filter = ('logic',)


admin.site.register(Achievement, AchievementAdmin)


class BadgeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Badge, BadgeAdmin)


