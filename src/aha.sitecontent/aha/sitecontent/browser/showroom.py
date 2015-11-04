# -*- coding: utf-8 -*-
"""Module providing views for the showroom content type"""
import math

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from OFS.interfaces import IOrderedContainer
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from aha.sitecontent.project import IProject
from zope.component import getMultiAdapter


class ShowRoomView(BrowserView):
    """ Show room default view """

    def render(self):
        return self.index()

    def __call__(self):
        self.has_showrooms = len(self.showrooms()) > 0
        self.has_subitems = len(self.subitems()) > 0
        return self.render()

    def showrooms(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@contentlisting')(
            portal_type='aha.sitecontent.showroom',
            review_state='published')

    def get_projects(self, item, preview=False):
        context = aq_inner(item)
        items = api.content.find(
            context=context,
            object_provides=IProject,
            review_state='published',
            sort_on='getObjPositionInParent',
            hasPreview=preview
        )
        return items

    def projects(self):
        context = aq_inner(self.context)
        if self.has_showrooms:
            projects = list()
            for showroom in self.showrooms():
                obj = showroom.getObject()
                showroom_projects = list(self.get_projects(obj, preview=True))
                projects = projects + showroom_projects
            return projects
        return list(self.get_projects(context))

    def subitems(self):
        """ A showroom containing other showrooms
            should not list contained projects
        """
        if self.has_showrooms:
            return self.showrooms()
        return self.projects()

    def content_matrix(self):
        items = self.projects()
        count = len(items)
        rowcount = count / 2.0
        rows = math.ceil(rowcount)
        matrix = []
        for i in range(int(rows)):
            row = []
            for j in range(2):
                index = 2 * i + j
                if index <= int(count - 1):
                    cell = {}
                    cell['item'] = items[index]
                    row.append(cell)
            matrix.append(row)
        return matrix

    def preview_image(self, item):
        return self._get_scaled_img(item, 'original')

    def computed_inline_styles(self, item):
        img = self.preview_image(item)
        base = BG = 'background:url({0}) no-repeat 50% 50% transparent;'.format(
            img['url']
        )
        bg_style = 'background-size: cover;'
        style = '{0}{1}'.format(base, bg_style)
        return style

    def image_tag(self, item):
        data = {}
        sizes = ['small', 'medium', 'large', 'original']
        idx = 0
        for size in sizes:
            idx += 0
            img = self._get_scaled_img(item, size)
            data[size] = '{0} {1}w'.format(img['url'], img['width'])
        return data

    def _get_scaled_img(self, item, size):
        if (
            ICatalogBrain.providedBy(item) or
            IContentListingObject.providedBy(item)
        ):
            obj = item.getObject()
        else:
            obj = item
        info = {}
        if hasattr(obj, 'image'):
            scales = getMultiAdapter((obj, self.request), name='images')
            if size == 'small':
                scale = scales.scale('image', width=300, height=300)
            if size == 'medium':
                scale = scales.scale('image', width=600, height=600)
            if size == 'large':
                scale = scales.scale('image', width=900, height=900)
            else:
                scale = scales.scale('image', width=1200, height=1200)
            if scale is not None:
                info['url'] = scale.url
                info['width'] = scale.width
                info['height'] = scale.height
            else:
                info['url'] = IMG
                info['width'] = '1px'
                info['height'] = '1px'
        else:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info
