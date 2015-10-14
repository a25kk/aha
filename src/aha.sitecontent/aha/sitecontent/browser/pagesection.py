# -*- coding: utf-8 -*-
"""Module providing views for a contentpage section"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.component import getUtility

from aha.sitecontent.interfaces import IResponsiveImagesTool


class PageSectionView(BrowserView):
    """ Page Section default view """

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def rendered_page_snippet(self):
        context = aq_inner(self.context)
        snippet = context.restrictedTraverse('@@pagesection-snippet')()
        return snippet


class PageSectionSnippet(BrowserView):
    """ Embeddable section content snippet """

    def field_has_data(self, fieldname):
        """ Check wether a given schema key returns a value"""
        context = aq_inner(self.context)
        try:
            video_link = getattr(context, fieldname, None)
        except AttributeError:
            video_link = None
        if video_link is not None:
            return True
        return False

    def has_video_link(self):
        return self.field_has_data('videoLink')

    def has_external_image(self):
        return self.field_has_data('externalImage')

    def show_image(self):
        display = True
        if self.has_video_link() or self.has_external_image():
            display = False
        return display

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)
