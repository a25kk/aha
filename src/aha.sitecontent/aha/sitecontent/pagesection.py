# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer
from zope import schema

from aha.sitecontent import _


class IPageSection(model.Schema, IImageScaleTraversable):
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

    model.fieldset(
        'display',
        label=u"Display",
        fields=['displayInquiryForm']
    )

    displayInquiryForm = schema.Bool(
        title=_(u"Check to enable inquiry form display"),
        description=_(u"When activated the view will attempt to display a "
                      u"web form inside the given page component"),
        required=False,
    )


@implementer(IPageSection)
class PageSection(Container):
    pass
