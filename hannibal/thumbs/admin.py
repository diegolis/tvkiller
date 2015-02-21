# -*- coding: utf-8 -*-
"""
Definitions for django admin
"""

from django.contrib import admin
from .models import (Channel,
                     Origin,
                     Clip,
                     Thumb)


admin.site.register(Channel)
admin.site.register(Origin)
admin.site.register(Clip)
admin.site.register(Thumb)
