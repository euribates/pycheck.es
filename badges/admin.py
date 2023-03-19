import json

from django.contrib import admin
from django.utils.html import format_html

from badges.models import Achievement, Badge


class AchievementAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('name', 'symbol', 'as_logic', 'as_group_level')
    list_filter = ('logic', 'group', 'level')

    @admin.display(description='Grupo/Nivel')
    def as_group_level(self, obj):
        return f"{obj.group}/{obj.level}"

    @admin.display(description='Lógica')
    def as_logic(self, obj):
        try:
            params = json.loads(obj.params)
        except json.JSONDecodeError as err:
            return f"ERROR: {err}"
        return format_html(''.join([
            '<code>',
            f'{obj.logic}(',
            ', '.join([
                f'{name}={value!r}'
                for name, value in params.items()
            ]),
            ')',
            '</code>',
        ]))


class BadgeAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('pk', 'student', 'achievement', 'granted_at')
    list_filter = ('student', 'achievement')
    date_hierarchy = 'granted_at'


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Badge, BadgeAdmin)


