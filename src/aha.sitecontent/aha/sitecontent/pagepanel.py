# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from zope.interface import implementer
from zope import schema

from aha.sitecontent import MessageFactory as _


class IPagePanel(model.Schema, IImageScaleTraversable):
    """ A content page section
    """

    model.fieldset(
        'external',
        label=u"External Assets",
        fields=['animation', 'video']
    )

    animation = schema.TextLine(
        title=_(u"Animated GIF"),
        description=_(u"Enter external URL pointing to an animated gif"),
        required=False
    )
    video = schema.TextLine(
        title=_(u"Video Link"),
        description=_(u"Provide URL of embeddable YouTube video."
                      u"Note: this will override all added animations."),
        required=False
    )


@implementer(IPagePanel)
class PagePanel(Container):
    pass