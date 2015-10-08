# -*- coding: utf-8 -*-
"""Module providing views for a contentpage section"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.component import getUtility

from aha.sitecontent.interfaces import IResponsiveImagesTool


class PageSectionView(BrowserView):
    """ Page Section default view """

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def rendered_page_snippet(self):
        context = aq_inner(self.context)
        snippet = context.restrictedTraverse('@@pagesection-snippet')
        return snippet


class PageSectionSnippet(BrowserView):
    """ Embeddable section content snippet """

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)
