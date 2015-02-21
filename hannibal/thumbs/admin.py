# -*- coding: utf-8 -*-
"""
Definitions for django admin
"""

from django.contrib import admin
from .models import Channel, Origin


admin.site.register(Channel)
admin.site.register(Origin)