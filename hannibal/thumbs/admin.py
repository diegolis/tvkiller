# -*- coding: utf-8 -*-
"""
Definitionf for djang admin
"""

from django.contrib import admin
from .models import Channel


admin.site.register(Channel)
