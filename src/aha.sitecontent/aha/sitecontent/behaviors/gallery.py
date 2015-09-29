# -*- coding: utf-8 -*-
"""Module providing JSON storage for static asset assignments"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope import schema

from aha.sitecontent import _


@provider(IFormFieldProvider)
class IGalleryEnabled(model.Schema):
    """Behavior providing a checkbox to toggle gallery display"""

    model.fieldset(
        'display',
        label=u"Display",
        fields=['displayGallery', 'displayThumbnails']
    )

    displayGallery = schema.Bool(
        title=_(u"Check to enable gallery display"),
        description=_(u"When activated the view will attempt to display a "
                      u"gallery of all contained images"),
        required=False,
    )


@implementer(IGalleryEnabled)
@adapter(IDexterityContent)
class GalleryEnabled(object):

    def __init__(self, context):
        self.context = context
