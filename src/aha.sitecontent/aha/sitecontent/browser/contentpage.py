# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
import datetime
from Acquisition import aq_inner
from plone import api
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility

from aha.sitecontent.contentpage import IContentPage
from aha.sitecontent.interfaces import IResponsiveImagesTool
from aha.sitecontent.pagesection import IPageSection


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
            review_state='published',
            sort_on='getObjPositionInParent')
        return items

    def rendered_page_section(self, section_uid):
        context = api.content.get(UID=section_uid)
        template = context.restrictedTraverse('@@pagesection-snippet')()
        if context.displayInquiryForm:
            template = context.restrictedTraverse('@@page-section-form')()
        return template


class GalleryView(BrowserView):
    """Preview embeddable image gallery"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def contained_images(self):
        context = aq_inner(self.context)
        data = context.restrictedTraverse('@@folderListing')(
            portal_type='Image',
            sort_on='getObjPositionInParent')
        return data

    def rendered_gallery(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@gallery-snippet')()
        return template


class GallerySnippet(BrowserView):
    """Provide gallery of contained image content"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

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
            object_provides=IPageSection,
            review_state='published',
            sort_on='getObjPositionInParent'
        )
        return pages

    def has_news(self):
        return len(self.news()) > 0

    def rendered_page_section(self, section_uid):
        context = api.content.get(UID=section_uid)
        template = context.restrictedTraverse('@@pagesection-snippet')()
        return template


class JobListingView(BrowserView):
    """ Listing of all content pages located in a global news folder """

    def jobs(self):
        portal = api.portal.get()
        pages = api.content.find(
            context=portal['jobs'],
            object_provides=IPageSection,
            review_state='published',
            sort_on='getObjPositionInParent'
        )
        return pages

    def has_jobs(self):
        return len(self.jobs()) > 0

    def rendered_page_section(self, section_uid):
        context = api.content.get(UID=section_uid)
        template = context.restrictedTraverse('@@pagesection-snippet')()
        return template


class FormDispatchedView(BrowserView):
    """ Inquiry form dispatched

        Show thank you page with feedback on how and when the request
        was processed after successful submit of page section embedded
        inquiry form contents
    """

    def processed_timestamp(self):
        datetime_now = datetime.datetime.utcnow()
        now = datetime_now.replace(tzinfo=pytz.utc)
        timestamp_data = {
            'date': api.portal.get_localized_time(now),
            'time': api.portal.get_localized_time(now, time_only=True),
        }
        return timestamp_data
