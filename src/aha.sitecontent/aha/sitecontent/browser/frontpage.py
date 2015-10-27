# -*- coding: utf-8 -*-
"""Module providing views for the site navigation root"""
from Products.Five.browser import BrowserView
from plone import api

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


class FrontPageIntranet(BrowserView):
    """ Intranet frontpage providing a list of downloads """

    def __call__(self):
        return self.render()

    def render(self):
        if api.user.is_anonymous():
            return self.request.response.redirect(self.login_url())
        return self.index()

    def get_available_downloads(self):
        results = api.content.find(
            portal_type='File',
            sort_on='getObjPositionInParent',
            review_state='internally_published'
        )
        return results

    def login_url(self):
        portal_url = api.portal.get().absolute_url()
        return '{0}/login_form'.format(portal_url)

    def has_downloads(self):
        return len(self.get_available_downloads()) > 0

    def get_mimetype_icon(self, content_file):
        portal_url = api.portal.get().absolute_url()
        mtr = api.portal.get_tool(name="mimetypes_registry")
        mime = []
        if content_file.contentType:
            mime.append(mtr.lookup(content_file.contentType))
        if content_file.filename:
            mime.append(mtr.lookupExtension(content_file.filename))
        mime.append(mtr.lookup("application/octet-stream")[0])
        icon_paths = [m.icon_path for m in mime if hasattr(m, 'icon_path')]
        if icon_paths:
            return icon_paths[0]

        return portal_url + "/" + guess_icon_path(mime[0])
