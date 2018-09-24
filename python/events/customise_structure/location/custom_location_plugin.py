# :coding: utf-8
# :copyright: Copyright (c) 2018 ftrack

import functools
import logging

import ftrack_api
import ftrack_api.accessor.disk

import structure

logger = logging.getLogger('ftrack-example-location')

# Name of the location plugin.
LOCATION_NAME = 'custom_location'

# Disk mount point.
DISK_PREFIX = ''


def configure_location(session, event):
    '''Listen.'''
    location = session.ensure('Location', {'name': LOCATION_NAME})

    location.accessor = ftrack_api.accessor.disk.DiskAccessor(
        prefix=DISK_PREFIX
    )
    location.structure = structure.Structure()
    location.priority = 1

    logger.info(
        u'Registered location {0} at {1}.'.format(LOCATION_NAME, DISK_PREFIX)
    )


def register(session, **kw):
    '''Register location with *session*.'''

    if not isinstance(session, ftrack_api.Session):
        return

    if not DISK_PREFIX:
        logger.info('No disk prefix configured for location.')
        return

    session.event_hub.subscribe(
        'topic=ftrack.api.session.configure-location',
        functools.partial(configure_location, session)
    )
