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
    cms_plugin_base = 'cms.plugin_base.CMSPluginBase'
    plugin_base = getattr(settings, 'BOOTSTRAP3_PLUGIN_BASE', cms_plugin_base)
    plugin_base_class = plugin_base.split('.')[-1]
    plugin_base_module = plugin_base.replace(plugin_base_class, '')
    mod = __import__(plugin_base_module, fromlist=[plugin_base_class, ])
    return getattr(mod, plugin_base_class)
