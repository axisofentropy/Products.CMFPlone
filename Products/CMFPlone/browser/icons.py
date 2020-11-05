# -*- coding: utf-8 -*-
from OFS.Image import File
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import ISiteRoot
from zExceptions import NotFound
from zope.component import adapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface
from zope.location.interfaces import LocationError
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import IPublishTraverse

import logging

logger = logging.getLogger(__name__)


@implementer(IPublishTraverse)
class IconsView(BrowserView):

    prefix = "plone.icon."

    def publishTraverse(self, request, name):
        self.name = name
        return self

    def __call__(self):
        name = getattr(self, 'name', None)
        if name is None:
            raise NotFound("No name were given as subpath.")
        fileobj = getSite().restrictedTraverse(self.lookup(self.name))
        return fileobj(REQUEST=self.request, RESPONSE=self.request.response)

    def lookup(self, name):
        registry = getUtility(IRegistry)
        icon = self.prefix + name
        try:
            return registry[icon]
        except KeyError:
            logger.exception(f"Icon resolver lookup of '{name}' failed, fallback to Plone icon.")
            return "++plone++icons/plone.svg"

    def url(self, name):
        url = getSite().absolute_url() + "/" + self.lookup(name)
        return url

    def tag(self, name, tag_class="", tag_alt=""):
        icon = self.lookup(name)
        if not icon.endswith(".svg"):
            return f'<img src="{self.url(name)}" class="{tag_class}" alt="{tag_alt}" />'

        iconfile = getSite().restrictedTraverse(icon)
        if isinstance(iconfile, File):
            raise NotImplementedError(
                "Resolve icons stored in database is not yet implemented."
            )
        with open(iconfile.path, "rb") as fh:
            return fh.read()