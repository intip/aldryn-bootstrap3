# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from .conf import settings


def get_additional_styles():
    """
    Get additional styles choices from settings
    """
    choices = []
    raw = getattr(settings, 'GALLERY_STYLES', False)
    if raw:
        if isinstance(raw, basestring):
            raw = raw.split(',')
        for choice in raw:
            clean = choice.strip()
            choices.append((clean.lower(), clean.title()))
    return choices


def get_plugin_base():
    plugin_base = getattr(settings, 'BOOTSTRAP3_PLUGIN_BASE')
    mod = __import__(plugin_base)
    components = plugin_base.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
