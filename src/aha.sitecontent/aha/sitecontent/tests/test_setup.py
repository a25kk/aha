# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from aha.sitecontent.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of aha.sitecontent into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if aha.sitecontent is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('aha.sitecontent'))

    def test_uninstall(self):
        """Test if aha.sitecontent is cleanly uninstalled."""
        self.installer.uninstallProducts(['aha.sitecontent'])
        self.assertFalse(self.installer.isProductInstalled('aha.sitecontent'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IAhaSitecontentLayer is registered."""
        from aha.sitecontent.interfaces import IAhaSitecontentLayer
        from plone.browserlayer import utils
        self.failUnless(IAhaSitecontentLayer in utils.registered_layers())
