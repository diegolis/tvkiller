# -*- coding: utf-8 -*-
"""
Definitions for django admin
"""

from django.contrib import admin


from .models import (Channel,
                     Origin,
                     Clip,
                     Thumb)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_name', 'device_slot']

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Origin)
admin.site.register(Clip)
admin.site.register(Thumb)
