# -*- coding: utf-8 -*-
"""Module providing showroom content type functionality"""

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer


class IShowRoom(form.Schema, IImageScaleTraversable):
    """
    A folderish page
    """


@implementer(IShowRoom)
class ShowRoom(Container):
    pass
