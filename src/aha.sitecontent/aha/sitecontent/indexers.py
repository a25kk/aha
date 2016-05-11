# -*- coding: utf-8 -*-
"""Module providing a custom indexing setup for sitecontent"""
from plone.indexer.decorator import indexer
from aha.sitecontent.project import IProject


def _unicode_save_string_concat(*args):
    """
    Concat args with spaces between and returns utf-8 string, it does not
    matter if input was unicode or str
    """
    result = ''
    for value in args:
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'replace')
        result = ' '.join((result, value))
    return result


@indexer(IProject)
def has_preview_project(obj):
    if obj.hasPreview is None:
        return None
    return obj.hasPreview
