# -*- coding: utf-8 -*-
"""
Definitions for django admin
"""

from django.contrib import admin
from .models import Channel


admin.site.register(Channel)
