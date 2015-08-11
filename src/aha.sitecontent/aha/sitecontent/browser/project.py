# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
import json
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class ProjectView(BrowserView):
    """ Show room default view """

    def __call__(self):
        self.has_assets = len(self.assets()) > 0
        return self.render()

    def render(self):
        return self.index()

    def can_edit(self):
        show = False
        if not api.user.is_anonymous():
            show = True
        return show

    def assets(self):
        context = aq_inner(self.context)
        data = getattr(context, 'assets')
        if data is None:
            data = dict()
        return data

    def stored_data(self):
        return json.loads(self.assets())

    def image_list(self):
        data = self.stored_data()
        items = data['items']
        images = list()
        for item in items:
            item_uid = str(item)
            catalog = api.portal.get_tool(name='portal_catalog')
            stack = catalog.unrestrictedSearchResults(UID=item_uid)
            obj = stack[0].getObject()
            contained_imgs = obj.unrestrictedTraverse('@@folderListing')()
            for img in contained_imgs:
                img_uid = api.content.get_uuid(obj=img.getObject())
                images.append(img_uid)
        return images

    def image_tag(self, uuid):
        context = api.content.get(UID=uuid)
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image')
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item
