# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
import math
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from zope.component import getMultiAdapter
from aha.sitecontent.pagesection import IPageSection
from aha.sitecontent.contentpage import IContentPage

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class ContentPageView(BrowserView):
    """ Folderish content page default view """

    def __call__(self):
        self.has_subitems = len(self.contained_sections()) > 0
        return self.render()

    def render(self):
        return self.index()

    def contained_sections(self):
        context = aq_inner(self.context)
        items =  api.content.find(
            context=context,
            depth=1,
            object_provides=IPageSection,
            review_state='published'
        )
        return items

    def rendered_page_section(self, section_uid):
        context = api.content.get(UID=section_uid)
        template = context.restrictedTraverse('@@pagesection-snippet')()
        return template


class GalleryPreview(BrowserView):
    """Preview embeddable image gallery"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def rendered_gallery(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@gallery-view')()
        return template


class GalleryView(BrowserView):
    """Provide gallery of contained image content"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def has_leadimage(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def leadimage_tag(self):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image', width=900, height=900)
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

    def contained_images(self):
        context = aq_inner(self.context)
        data = context.restrictedTraverse('@@folderListing')(
            portal_type='Image',
            sort_on='getObjPositionInParent')
        return data[:9]

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)


class GalleryThumbnailView(BrowserView):
    """ Optional thumbnail overlay content """

    def contained_images(self):
        context = aq_inner(self.context)
        data = context.restrictedTraverse('@@folderListing')(
            portal_type='Image',
            sort_on='getObjPositionInParent'
        )
        return data[:9]

    def has_assets(self):
        return len(self.contained_images()) > 0

    def image_tag(self, image):
        context = image.getObject()
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image', width=120, height=120)
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


class NewsListingView(BrowserView):
    """ Listing of all content pages located in a global news folder """

    def news(self):
        portal = api.portal.get()
        pages = api.content.find(
            context=portal['aktuell'],
            object_provides=IContentPage,
            review_state='published',
            sort_on='getObjPositionInParent'
        )
        return pages

    def has_news(self):
        return len(self.news()) > 0

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
        try:
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
        except:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info


class JobListingView(BrowserView):
    """ Listing of all content pages located in a global news folder """

    def jobs(self):
        portal = api.portal.get()
        pages = api.content.find(
            context=portal['jobs'],
            object_provides=IContentPage,
            review_state='published',
            sort_on='getObjPositionInParent'
        )
        return pages

    def has_jobs(self):
        return len(self.jobs()) > 0

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
        try:
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
        except:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info
