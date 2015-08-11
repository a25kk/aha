# -*- coding: utf-8 -*-
"""Module providing views for the site navigation root"""
import json
from Products.Five.browser import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from zope.component import getMultiAdapter

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class FrontPageView(BrowserView):
    """ General purpose frontpage view """

    def __call__(self):
        self.has_projects = len(self.projects()) > 0
        return self.render()

    def render(self):
        return self.index()

    def can_edit(self):
        show = False
        if not api.user.is_anonymous():
            show = True
        return show

    def projects(self):
        portal = api.portal.get()
        context = portal['models']
        return context.restrictedTraverse('@@folderListing')(
            portal_type='aha.sitecontent.project',
            review_state='published')

    def _project_assets(self, uuid):
        project = api.content.get(UID=uuid)
        data = getattr(project, 'assets')
        if data is None:
            data = dict()
        return data

    def _assets(self, uuid):
        return json.loads(self._project_assets(uuid))

    def has_preview_image(self, uuid):
        """ Test if we have an available preview image """
        assets = self._assets(uuid)
        return len(assets['items']) > 0

    def get_preview_container(self, uuid):
        data = self._assets(uuid)
        items = data['items']
        return items[0]

    def rendered_preview_image(self, uuid):
        item = api.content.get(UID=uuid)
        return item.restrictedTraverse('@@stack-preview')()

    def computed_class(self, uuid):
        item = api.content.get(UID=uuid)
        item_cat = 'artist'
        subjects = item.Subject()
        if subjects:
            item_cat = subjects[0]
        klass = 'app-card-{0} {1}'.format(uuid, item_cat)
        return klass

    def available_filter(self):
        catalog = api.portal.get_tool('portal_catalog')
        return catalog.uniqueValuesFor('Subject')

    def image_tag(self, item):
        data = {}
        sizes = ['small', 'medium', 'large']
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
            else:
                scale = scales.scale('image', width=900, height=900)
            if scale is not None:
                info['url'] = scale.url
                info['width'] = scale.width
                info['height'] = scale.height
        else:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info
