# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from aha.buildout.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of aha.buildout into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if aha.buildout is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('aha.buildout'))

    def test_uninstall(self):
        """Test if aha.buildout is cleanly uninstalled."""
        self.installer.uninstallProducts(['aha.buildout'])
        self.assertFalse(self.installer.isProductInstalled('aha.buildout'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IAhaBuildoutLayer is registered."""
        from aha.buildout.interfaces import IAhaBuildoutLayer
        from plone.browserlayer import utils
        self.failUnless(IAhaBuildoutLayer in utils.registered_layers())
