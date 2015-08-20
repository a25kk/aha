# -*- coding: utf-8 -*-
"""Module providing custom navbar"""
from urlparse import urlsplit
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter


class NavBarView(BrowserView):
    """ General purpose frontpage view """

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def selectedTabs(self, default_tab='index_html', portal_tabs=()):
        plone_url = api.portal.get().absolute_url()
        plone_url_len = len(plone_url)
        request = self.request
        parent_request = request['PARENT_REQUEST']
        valid_actions = []
        url = parent_request['URL']
        path = url[plone_url_len:]
        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            if path.startswith(action_path + '/') or path == action_path:
                valid_actions.append((len(action_path), action['id']))
        valid_actions.sort()
        if valid_actions:
            return {'portal': valid_actions[-1][1]}
        return {'portal': default_tab}

    def section(self):
        portal = api.portal.get()
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        portal_tabs = portal_tabs_view.topLevelTabs()
        selected_tabs = self.selectedTabs(portal_tabs=portal_tabs)
        selected_section = selected_tabs['portal']
        if selected_section != 'index_html':
            section = portal[selected_section]
            return section.getId()
        return portal.getId()

    def active_navitem(self, section):
        context = aq_inner(self.context)
        request = self.request
        parent_request = request['PARENT_REQUEST']
        path = urlsplit(parent_request['URL']).path
        if section in path.split('/'):
            return True
        return False
