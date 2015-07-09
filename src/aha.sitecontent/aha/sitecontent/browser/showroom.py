# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
import json
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api


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
        return context.restrictedTraverse('@@folderListing')(
            portal_type='aha.sitecontent.showroom',
            review_state='published')

    def projects(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@folderListing')(
            portal_type='aha.sitecontent.project',
            review_state='published')

    def subitems(self):
        """ A showroom containing other showrooms
            should not list contained projects
        """
        if self.has_showrooms:
            return self.showrooms()
        return self.projects()

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
