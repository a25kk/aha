# coding=utf-8
""" Module providing custom installation routines """
import logging
from plone import api

PROFILE_ID = 'profile-aha.sitecontent:default'


def setupCatalogIndexes(logger=None):
    """ Add indexes to portal catalog and reindex content

    :param context: The plone site object
    :param logger:  Custom progress logger
    """
    if logger is None:
        logger = logging.getLogger('aha.sitecontent')

    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()

    # Catalog indexes to be added
    wanted = (
        ('hasPreview', 'BooleanIndex'),
    )

    indexables = []

    for name, meta_name in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_name)
            indexables.append(name)
            logger('Added {0} for field {1}'.format(meta_name, name))
    if len(indexables) > 0:
        logger.info('Indexing new indexes {0}'.format(
            ', '.join(indexables)
        ))
        catalog.manage_reindexIndex(ids=indexables)


def importVarious(context):
    """ Import staps handler """
    if context.readDataFile('aha.sitecontent-various.txt') in None:
        return
    portal = api.portal.get()
    setupCatalogIndexes(portal)
