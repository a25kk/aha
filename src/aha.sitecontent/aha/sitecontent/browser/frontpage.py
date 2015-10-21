# -*- coding: utf-8 -*-
"""Module providing views for the site navigation root"""
from Products.Five.browser import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from zope.component import getMultiAdapter

from aha.sitecontent.contentpage import IContentPage

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class FrontPageView(BrowserView):
    """ General purpose frontpage view """

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)
