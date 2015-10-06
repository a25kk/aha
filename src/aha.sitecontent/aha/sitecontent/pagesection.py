# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope import schema

from aha.sitecontent import _


class IPageSection(model.Schema):
    """ A content page section
    """

    externalImage = schema.TextLine(
        title=_(u"External Image"),
        description=_(u"Enter URL of externally hosted image asset "
                      u"link e.g. animated GIFs"),
        required=False
    )

    videoLink = schema.TextLine(
        title=_(u"Videolink"),
        description=_(u"Enter URL to embed external videos from YouTube"),
        required=False
    )


@implementer(IPageSection)
class PageSection(Container):
    pass
