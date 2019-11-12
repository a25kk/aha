# -*- coding: utf-8 -*-
"""Module providing display options"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope import schema

from aha.sitecontent import _


@provider(IFormFieldProvider)
class IPreviewEnabled(model.Schema):
    """Behavior providing a checkbox to toggle visibility in listings"""

    model.fieldset(
        'display',
        label=u"Display",
        fields=['hasPreview']
    )

    hasPreview = schema.Bool(
        title=_(u"Check, if this item should include a preview snippet in "
                u"listings"),
        required=False,
        default=True
    )


@implementer(IPreviewEnabled)
@adapter(IDexterityContent)
class PreviewEnabled(object):

    def __init__(self, context):
        self.context = context
