# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import ftrack_connect_cinesync.cinesync_launcher


def register(registry, **kw):
    '''Register cineSync launch hooks.'''
    action = ftrack_connect_cinesync.cinesync_launcher.CinesyncLauncher()
    action.register()
