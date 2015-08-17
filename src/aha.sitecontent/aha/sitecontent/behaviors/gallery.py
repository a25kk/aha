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
        fields=['displayCards', 'displayGallery', 'displayThumbnails']
    )

    displayCards = schema.Bool(
        title=_(u"Enable preview cards"),
        description=_(u"Activate preview card listing of contained items."
                      u"This will override all other display options when "
                      u"activated"),
        required=False,
    )

    displayGallery = schema.Bool(
        title=_(u"Check to enable gallery display"),
        description=_(u"When activated the view will attempt to display a "
                      u"gallery of all contained images"),
        required=False,
    )
    displayThumbnails = schema.Bool(
        title=_(u"Check to enable thumbnail previews"),
        description=_(u"Setting will trigger thumbnail overlays with galley "
                      u"preview thumbnails and description"),
        required=False,
    )


@implementer(IGalleryEnabled)
@adapter(IDexterityContent)
class GalleryEnabled(object):

    def __init__(self, context):
        self.context = context
