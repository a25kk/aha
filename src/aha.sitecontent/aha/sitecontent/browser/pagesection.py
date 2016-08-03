# -*- coding: utf-8 -*-
"""Module providing views for a contentpage section"""
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from plone.protect.utils import addTokenToUrl
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility

from aha.sitecontent.mailer import create_plaintext_message
from aha.sitecontent.mailer import prepare_email_message
from aha.sitecontent.mailer import get_mail_template
from aha.sitecontent.mailer import send_mail

from aha.sitecontent.interfaces import IResponsiveImagesTool

from aha.sitecontent import _


class PageSectionView(BrowserView):
    """ Page Section default view """

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def parent_page(self):
        return aq_parent(aq_inner(self.context))

    def rendered_page_snippet(self):
        context = aq_inner(self.context)
        snippet = context.restrictedTraverse('@@pagesection-snippet')()
        if context.displayInquiryForm:
            snippet = context.restrictedTraverse('@@page-section-form')()
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


class PageSectionForm(BrowserView):
    """ Embeddable section content snippet including inquiry form """

    def __call__(self):
        self.errors = {}
        return self.render()

    def update(self):
        translation_service = api.portal.get_tool(name="translation_service")
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ['email']
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error_msg = _(u"This field is required")
                        error['active'] = True
                        error['msg'] = translation_service.translate(
                            error_msg,
                            'aha.sitecontent',
                            target_language=api.portal.get_default_language()
                        )
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self.send_inquiry(form)

    def render(self):
        self.update()
        return self.index()

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value

    def send_inquiry(self, data):
        context = aq_inner(self.context)
        subject = _(u"Inquiry from website visitor")
        email_subject = api.portal.translate(
            "Inquiry from website visitor",
            'aha.sitecontent',
            api.portal.get_current_language())
        data['subject'] = email_subject
        mail_tpl = self._compose_message(data)
        mail_plain = create_plaintext_message(mail_tpl)
        msg = prepare_email_message(mail_tpl, mail_plain)
        recipients = ['service@aha360.com', ]
        send_mail(
            msg,
            recipients,
            email_subject
        )
        context_parent = aq_parent(context)
        next_url = '{0}/@@inquiry-form-dispatched/'.format(
            context_parent.absolute_url()
        )
        url = addTokenToUrl(next_url)
        return self.request.response.redirect(url)

    def _compose_message(self, data):
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        template_vars = {
            'email': data['email'],
            'subject': str(data['subject']),
            'fullname': data['fullname'],
            'phone': data['phone'],
            'message': data['comment'],
            'url': portal_url
        }
        template_name = 'inquiry-mail.html'
        message = get_mail_template(template_name, template_vars)
        return message

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
